import secrets
from functools import wraps

from flask import (
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from .db import get_db
from .services import (
    ReservationConflict,
    ValidationError,
    available_seats,
    confirm_reservation,
    create_customer,
    create_film,
    create_room,
    create_screening,
    get_schedule,
    review_reservation,
)


def register_routes(app):
    @app.before_request
    def protect_forms_and_load_account():
        if request.method == "POST":
            expected = session.get("_csrf_token")
            supplied = request.form.get("csrf_token", "")
            if not expected or not secrets.compare_digest(expected, supplied):
                abort(400, description="Token de formulário inválido ou expirado.")
        account_id = session.get("account_id")
        g.account = None
        if account_id:
            g.account = get_db().execute(
                "SELECT id, username, role FROM accounts WHERE id = ?",
                (account_id,),
            ).fetchone()
            if g.account is None:
                session.clear()

    @app.context_processor
    def inject_template_helpers():
        def csrf_token():
            if "_csrf_token" not in session:
                session["_csrf_token"] = secrets.token_urlsafe(32)
            return session["_csrf_token"]

        return {"csrf_token": csrf_token, "account": g.get("account")}

    def roles_required(*roles):
        def decorate(view):
            @wraps(view)
            def wrapped(*args, **kwargs):
                account = g.get("account")
                if account is None:
                    return redirect(url_for("login", next=request.path))
                if account["role"] != "admin" and account["role"] not in roles:
                    abort(403)
                return view(*args, **kwargs)

            return wrapped

        return decorate

    @app.get("/")
    def home():
        films = get_db().execute(
            """SELECT films.*, screenings.id AS screening_id, screenings.starts_at,
                      screenings.duration_minutes, screenings.ticket_price_cents,
                      rooms.name AS room_name
            FROM films
            LEFT JOIN screenings ON screenings.film_id = films.id
                AND screenings.starts_at >= datetime('now', 'localtime')
            LEFT JOIN rooms ON rooms.id = screenings.room_id
            ORDER BY films.title, screenings.starts_at"""
        ).fetchall()
        return render_template("home.html", films=films)

    @app.route("/entrar", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = get_db().execute(
                "SELECT * FROM accounts WHERE username = ?", (username,)
            ).fetchone()
            if user is None or not check_password_hash(user["password_hash"], password):
                flash("Usuário ou senha inválidos.", "error")
            else:
                session.clear()
                session["account_id"] = user["id"]
                flash("Acesso realizado.", "success")
                destination = (
                    url_for("management")
                    if user["role"] in {"admin", "manager"}
                    else url_for("home")
                )
                return redirect(destination)
        return render_template("login.html")

    @app.post("/sair")
    def logout():
        session.clear()
        flash("Você saiu da aplicação.", "success")
        return redirect(url_for("home"))

    @app.get("/gestao")
    @roles_required("manager")
    def management():
        return render_template("management.html")

    @app.get("/gestao/cadastros/<kind>")
    @roles_required("manager")
    def list_records(kind):
        queries = {
            "salas": (
                "SELECT name, seat_count, opening_time, closing_time FROM rooms ORDER BY name",
                ("Sala", "Assentos", "Abre", "Fecha"),
            ),
            "filmes": (
                """SELECT title, duration_minutes, genre, rating, is_national
                FROM films ORDER BY title""",
                ("Filme", "Duração (min)", "Gênero", "Faixa etária", "Nacional"),
            ),
            "sessoes": (
                """SELECT films.title, screenings.starts_at, rooms.name,
                          screenings.duration_minutes, screenings.ticket_price_cents
                FROM screenings
                JOIN films ON films.id = screenings.film_id
                JOIN rooms ON rooms.id = screenings.room_id
                ORDER BY screenings.starts_at""",
                ("Filme", "Início", "Sala", "Duração (min)", "Ingresso (centavos)"),
            ),
            "clientes": (
                """SELECT name, age, email, city, state FROM customers ORDER BY name""",
                ("Cliente", "Idade", "E-mail", "Cidade", "Estado"),
            ),
        }
        if kind not in queries:
            abort(404)
        if kind == "clientes" and g.account["role"] != "admin":
            abort(403)
        query, headers = queries[kind]
        records = get_db().execute(query).fetchall()
        return render_template(
            "record_list.html",
            kind=kind,
            headers=headers,
            records=records,
        )

    @app.route("/gestao/salas/nova", methods=["GET", "POST"])
    @roles_required("manager")
    def new_room():
        if request.method == "POST":
            try:
                create_room(request.form)
            except ValidationError as error:
                flash(str(error), "error")
            except Exception:
                app.logger.exception("Falha ao cadastrar sala")
                flash("Não foi possível concluir o cadastro da sala.", "error")
            else:
                flash("Sala cadastrada.", "success")
                return redirect(url_for("new_room"))
        return render_template("room_form.html")

    @app.route("/gestao/filmes/novo", methods=["GET", "POST"])
    @roles_required("manager")
    def new_film():
        if request.method == "POST":
            try:
                create_film(request.form)
            except ValidationError as error:
                flash(str(error), "error")
            except Exception:
                app.logger.exception("Falha ao cadastrar filme")
                flash("Não foi possível concluir o cadastro do filme.", "error")
            else:
                flash("Filme cadastrado.", "success")
                return redirect(url_for("new_film"))
        return render_template("film_form.html")

    @app.route("/gestao/sessoes/nova", methods=["GET", "POST"])
    @roles_required("manager")
    def new_screening():
        db = get_db()
        films = db.execute("SELECT id, title FROM films ORDER BY title").fetchall()
        rooms = db.execute("SELECT id, name FROM rooms ORDER BY name").fetchall()
        if request.method == "POST":
            try:
                create_screening(request.form)
            except ValidationError as error:
                flash(str(error), "error")
            except Exception:
                app.logger.exception("Falha ao cadastrar sessão")
                flash("Não foi possível concluir o cadastro da sessão.", "error")
            else:
                flash("Sessão cadastrada.", "success")
                return redirect(url_for("new_screening"))
        return render_template("screening_form.html", films=films, rooms=rooms)

    @app.get("/gestao/programacao")
    @roles_required("manager")
    def schedule():
        day = request.args.get("dia", "")
        screenings, has_national = get_schedule(day) if day else ([], False)
        return render_template(
            "schedule.html",
            day=day,
            screenings=screenings,
            has_national=has_national,
        )

    @app.get("/cadastro")
    def customer_registration():
        return render_template("customer_form.html")

    @app.post("/cadastro")
    def register_customer():
        try:
            customer_id = create_customer(request.form)
        except ValidationError as error:
            flash(str(error), "error")
        except Exception as error:
            if "customers.email" in str(error) or "UNIQUE constraint failed" in str(error):
                flash("Este e-mail já cadastrado. Informe outro e-mail.", "error")
            else:
                app.logger.exception("Falha ao cadastrar cliente")
                flash("Não foi possível concluir o cadastro.", "error")
        else:
            session["customer_id"] = customer_id
            flash("Cadastro realizado.", "success")
            return redirect(url_for("home"))
        return render_template("customer_form.html"), 400

    @app.get("/sessoes/<int:screening_id>/assentos")
    def seat_selection(screening_id):
        screening = get_db().execute(
            """SELECT screenings.*, films.title AS film_title, rooms.name AS room_name
            FROM screenings JOIN films ON films.id = screenings.film_id
            JOIN rooms ON rooms.id = screenings.room_id
            WHERE screenings.id = ?""",
            (screening_id,),
        ).fetchone()
        if screening is None:
            abort(404)
        if not session.get("customer_id"):
            flash("Cadastre-se antes de escolher os assentos.", "info")
            return redirect(url_for("customer_registration"))
        return render_template(
            "seats.html",
            screening=screening,
            seats=available_seats(screening_id),
        )

    @app.post("/reservas/revisar/<int:screening_id>")
    def review_booking(screening_id):
        customer_id = session.get("customer_id")
        if not customer_id:
            flash("Cadastre-se para continuar com a reserva.", "info")
            return redirect(url_for("customer_registration"))
        try:
            screening, customer, seats = review_reservation(
                screening_id,
                request.form.getlist("assento_ids"),
                customer_id,
            )
        except (ValidationError, ReservationConflict) as error:
            flash(str(error), "error")
            return redirect(url_for("seat_selection", screening_id=screening_id))
        session["pending_booking"] = {
            "screening_id": screening_id,
            "customer_id": customer["id"],
            "seat_ids": [seat["id"] for seat in seats],
            "idempotency_key": secrets.token_urlsafe(24),
        }
        return render_template(
            "booking_review.html",
            screening=screening,
            customer=customer,
            seats=seats,
        )

    @app.get("/reservas/revisar")
    def booking_review():
        pending = session.get("pending_booking")
        if not pending or pending["customer_id"] != session.get("customer_id"):
            flash("Não há reserva aguardando confirmação.", "error")
            return redirect(url_for("home"))
        try:
            screening, customer, seats = review_reservation(
                pending["screening_id"],
                pending["seat_ids"],
                pending["customer_id"],
            )
        except (ValidationError, ReservationConflict) as error:
            session.pop("pending_booking", None)
            flash(str(error), "error")
            return redirect(url_for("seat_selection", screening_id=pending["screening_id"]))
        return render_template(
            "booking_review.html",
            screening=screening,
            customer=customer,
            seats=seats,
        )

    @app.post("/reservas/confirmar")
    def confirm_booking():
        pending = session.get("pending_booking")
        if not pending or pending["customer_id"] != session.get("customer_id"):
            flash("Não há reserva aguardando confirmação.", "error")
            return redirect(url_for("home"))
        try:
            batch_id, reservation_ids = confirm_reservation(
                pending["screening_id"],
                pending["customer_id"],
                pending["seat_ids"],
                pending["idempotency_key"],
            )
        except (ValidationError, ReservationConflict) as error:
            session.pop("pending_booking", None)
            flash(str(error), "error")
            return redirect(url_for("home"))
        except Exception:
            app.logger.exception("Falha ao confirmar reserva")
            flash("Não foi possível confirmar a reserva. Tente novamente.", "error")
            return redirect(url_for("booking_review"))
        session.pop("pending_booking", None)
        return redirect(url_for("booking_confirmation", batch_id=batch_id))

    @app.get("/reservas/<int:batch_id>")
    def booking_confirmation(batch_id):
        customer_id = session.get("customer_id")
        if not customer_id:
            abort(403)
        db = get_db()
        batch = db.execute(
            """SELECT reservation_batches.id, screenings.starts_at, films.title,
                      rooms.name AS room_name, customers.name AS customer_name,
                      customers.id AS customer_id
            FROM reservation_batches
            JOIN screenings ON screenings.id = reservation_batches.screening_id
            JOIN films ON films.id = screenings.film_id
            JOIN rooms ON rooms.id = screenings.room_id
            JOIN customers ON customers.id = reservation_batches.customer_id
            WHERE reservation_batches.id = ?""",
            (batch_id,),
        ).fetchone()
        if batch is None:
            abort(404)
        if batch["customer_id"] != customer_id:
            abort(403)
        reservations = db.execute(
            """SELECT seats.label, reservations.price_cents
            FROM reservations JOIN seats ON seats.id = reservations.seat_id
            WHERE reservations.batch_id = ? ORDER BY CAST(seats.label AS INTEGER)""",
            (batch_id,),
        ).fetchall()
        return render_template(
            "booking_confirmation.html",
            batch=batch,
            reservations=reservations,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return render_template("error.html", code=400, message=error.description), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template(
            "error.html", code=403, message="Você não tem permissão para esta operação."
        ), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template(
            "error.html", code=404, message="O conteúdo solicitado não foi encontrado."
        ), 404
