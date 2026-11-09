import hashlib
import json
from datetime import datetime, time, timedelta
from decimal import Decimal, InvalidOperation

from .db import get_db


class ValidationError(ValueError):
    pass


class ReservationConflict(ValueError):
    pass


def _required(data, key, label):
    value = data.get(key, "").strip()
    if not value:
        raise ValidationError(f"O campo {label} é obrigatório.")
    return value


def _positive_int(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValidationError(f"{label} deve ser um número inteiro.") from error
    if parsed <= 0:
        raise ValidationError(f"{label} deve ser maior que zero.")
    return parsed


def _nonnegative_int(value, label):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValidationError(f"{label} deve ser um número inteiro.") from error
    if parsed < 0:
        raise ValidationError(f"{label} não pode ser negativo.")
    return parsed


def create_room(data):
    db = get_db()
    name = _required(data, "nome", "nome")
    seat_count = _positive_int(data.get("quantidade_assentos"), "Quantidade de assentos")
    opening = _required(data, "horario_abertura", "horário de abertura")
    closing = _required(data, "horario_fechamento", "horário de fechamento")
    specification = _required(data, "especificacao_tecnica", "especificação técnica")
    try:
        if datetime.strptime(opening, "%H:%M") >= datetime.strptime(closing, "%H:%M"):
            raise ValidationError("O fechamento deve ocorrer depois da abertura no mesmo dia.")
    except ValueError as error:
        raise ValidationError("Informe horários válidos.") from error
    try:
        db.execute("BEGIN IMMEDIATE")
        cursor = db.execute(
            """INSERT INTO rooms
            (name, seat_count, opening_time, closing_time, technical_specification)
            VALUES (?, ?, ?, ?, ?)""",
            (name, seat_count, opening, closing, specification),
        )
        room_id = cursor.lastrowid
        db.executemany(
            "INSERT INTO seats (room_id, label) VALUES (?, ?)",
            [(room_id, str(index)) for index in range(1, seat_count + 1)],
        )
        db.commit()
        return room_id
    except Exception:
        db.rollback()
        raise


def create_film(data):
    title = _required(data, "titulo", "título")
    duration = _positive_int(data.get("duracao_minutos"), "Duração")
    genre = _required(data, "genero", "gênero")
    synopsis = _required(data, "sinopse", "sinopse")
    poster_url = _required(data, "cartaz_url", "URL do cartaz")
    if not poster_url.startswith(("https://", "http://")):
        raise ValidationError("A URL do cartaz deve usar HTTP ou HTTPS.")
    rating = _required(data, "faixa_etaria", "faixa etária")
    cast = _required(data, "elenco", "elenco")
    is_national = 1 if data.get("nacional") == "on" else 0
    cursor = get_db().execute(
        """INSERT INTO films
        (title, duration_minutes, genre, synopsis, poster_url, rating, cast_description, is_national)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (title, duration, genre, synopsis, poster_url, rating, cast, is_national),
    )
    get_db().commit()
    return cursor.lastrowid


def create_screening(data):
    db = get_db()
    film_id = _positive_int(data.get("filme_id"), "Filme")
    room_id = _positive_int(data.get("sala_id"), "Sala")
    start_text = _required(data, "inicio", "início da sessão")
    duration = _positive_int(data.get("duracao_minutos"), "Duração")
    try:
        starts_at = datetime.fromisoformat(start_text)
    except ValueError as error:
        raise ValidationError("Informe uma data e horário válidos.") from error
    if starts_at.tzinfo is not None:
        raise ValidationError("Informe o horário local sem fuso horário.")
    price_text = _required(data, "valor_ingresso", "valor do ingresso").replace(",", ".")
    try:
        price = Decimal(price_text)
        if not price.is_finite() or price != price.quantize(Decimal("0.01")):
            raise InvalidOperation
        price_cents = int(price * 100)
    except InvalidOperation as error:
        raise ValidationError("Informe um valor de ingresso válido.") from error
    if price_cents < 0:
        raise ValidationError("O valor do ingresso não pode ser negativo.")
    room = db.execute(
        "SELECT opening_time, closing_time FROM rooms WHERE id = ?", (room_id,)
    ).fetchone()
    film = db.execute(
        "SELECT duration_minutes FROM films WHERE id = ?", (film_id,)
    ).fetchone()
    if room is None or film is None:
        raise ValidationError("Selecione uma sala e um filme cadastrados.")
    if duration < film["duration_minutes"]:
        raise ValidationError("A sessão não pode ser mais curta que o filme.")
    session_start = starts_at.time()
    session_end_at = starts_at + timedelta(minutes=duration)
    if session_end_at.date() != starts_at.date():
        raise ValidationError("A sessão deve terminar no mesmo dia em que começa.")
    opening = time.fromisoformat(room["opening_time"])
    closing = time.fromisoformat(room["closing_time"])
    if session_start < opening or session_end_at.time() > closing:
        raise ValidationError("A sessão deve ocorrer dentro do horário de funcionamento da sala.")
    cursor = db.execute(
        """INSERT INTO screenings
        (film_id, room_id, starts_at, duration_minutes, ticket_price_cents)
        VALUES (?, ?, ?, ?, ?)""",
        (film_id, room_id, starts_at.isoformat(timespec="minutes"), duration, price_cents),
    )
    db.commit()
    return cursor.lastrowid


def create_customer(data):
    name = _required(data, "nome", "nome")
    age = _nonnegative_int(data.get("idade"), "Idade")
    if age > 130:
        raise ValidationError("Informe uma idade válida.")
    email = _required(data, "email", "e-mail").lower()
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        raise ValidationError("Informe um e-mail válido.")
    values = (
        name,
        age,
        email,
        _required(data, "logradouro", "logradouro"),
        _required(data, "numero", "número"),
        data.get("complemento", "").strip(),
        _required(data, "bairro", "bairro"),
        _required(data, "cidade", "cidade"),
        _required(data, "estado", "estado"),
        _required(data, "cep", "CEP"),
    )
    cursor = get_db().execute(
        """INSERT INTO customers
        (name, age, email, street, number, complement, neighborhood, city, state, postal_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        values,
    )
    get_db().commit()
    return cursor.lastrowid


def available_seats(screening_id):
    return get_db().execute(
        """SELECT seats.id, seats.label
        FROM seats
        JOIN screenings ON screenings.room_id = seats.room_id
        WHERE screenings.id = ?
          AND NOT EXISTS (
              SELECT 1 FROM reservations
              WHERE reservations.screening_id = screenings.id
                AND reservations.seat_id = seats.id
          )
        ORDER BY CAST(seats.label AS INTEGER)""",
        (screening_id,),
    ).fetchall()


def review_reservation(screening_id, seat_ids, customer_id):
    db = get_db()
    screening = db.execute(
        """SELECT screenings.*, films.title AS film_title, rooms.name AS room_name
        FROM screenings
        JOIN films ON films.id = screenings.film_id
        JOIN rooms ON rooms.id = screenings.room_id
        WHERE screenings.id = ?""",
        (screening_id,),
    ).fetchone()
    customer = db.execute(
        "SELECT id, name, email FROM customers WHERE id = ?", (customer_id,)
    ).fetchone()
    if screening is None or customer is None:
        raise ValidationError("A sessão ou o cadastro não está disponível.")
    unique_ids = sorted({int(value) for value in seat_ids})
    if not unique_ids:
        raise ValidationError("Selecione ao menos um assento.")
    placeholders = ",".join("?" for _ in unique_ids)
    seats = db.execute(
        f"""SELECT id, label FROM seats
        WHERE room_id = ? AND id IN ({placeholders})""",
        (screening["room_id"], *unique_ids),
    ).fetchall()
    if len(seats) != len(unique_ids):
        raise ValidationError("A seleção contém assentos que não pertencem a essa sala.")
    taken = db.execute(
        f"""SELECT 1 FROM reservations
        WHERE screening_id = ? AND seat_id IN ({placeholders}) LIMIT 1""",
        (screening_id, *unique_ids),
    ).fetchone()
    if taken:
        raise ReservationConflict("Um ou mais assentos não estão mais disponíveis.")
    return screening, customer, seats


def confirm_reservation(screening_id, customer_id, seat_ids, idempotency_key):
    db = get_db()
    normalized_ids = sorted({int(value) for value in seat_ids})
    request_hash = hashlib.sha256(
        json.dumps(
            [screening_id, customer_id, normalized_ids], separators=(",", ":")
        ).encode()
    ).hexdigest()
    try:
        db.execute("BEGIN IMMEDIATE")
        previous = db.execute(
            """SELECT id, request_hash FROM reservation_batches
            WHERE idempotency_key = ?""",
            (idempotency_key,),
        ).fetchone()
        if previous:
            if previous["request_hash"] != request_hash:
                raise ReservationConflict("A chave de confirmação já foi usada.")
            reservations = db.execute(
                "SELECT id FROM reservations WHERE batch_id = ? ORDER BY id",
                (previous["id"],),
            ).fetchall()
            db.commit()
            return previous["id"], [row["id"] for row in reservations]

        screening = db.execute(
            "SELECT * FROM screenings WHERE id = ?", (screening_id,)
        ).fetchone()
        if screening is None:
            raise ValidationError("A sessão não está disponível.")
        starts_at = datetime.fromisoformat(screening["starts_at"])
        ends_at = starts_at + timedelta(minutes=screening["duration_minutes"])
        existing = db.execute(
            """SELECT screenings.starts_at, screenings.duration_minutes
            FROM reservations
            JOIN screenings ON screenings.id = reservations.screening_id
            WHERE reservations.customer_id = ? AND screenings.id <> ?""",
            (customer_id, screening_id),
        ).fetchall()
        for row in existing:
            existing_start = datetime.fromisoformat(row["starts_at"])
            existing_end = existing_start + timedelta(minutes=row["duration_minutes"])
            if existing_start < ends_at and existing_end > starts_at:
                raise ReservationConflict(
                    "Esta sessão conflita com outra reserva sua."
                )

        seat_ids = normalized_ids
        if not seat_ids:
            raise ValidationError("Selecione ao menos um assento.")
        batch_cursor = db.execute(
            """INSERT INTO reservation_batches
            (idempotency_key, request_hash, customer_id, screening_id)
            VALUES (?, ?, ?, ?)""",
            (idempotency_key, request_hash, customer_id, screening_id),
        )
        batch_id = batch_cursor.lastrowid
        placeholders = ",".join("?" for _ in seat_ids)
        seats = db.execute(
            f"SELECT id FROM seats WHERE room_id = ? AND id IN ({placeholders})",
            (screening["room_id"], *seat_ids),
        ).fetchall()
        if len(seats) != len(seat_ids):
            raise ValidationError("A seleção contém assentos de outra sala.")
        reservation_ids = []
        for seat_id in seat_ids:
            cursor = db.execute(
                """INSERT INTO reservations
                (batch_id, customer_id, screening_id, room_id, seat_id, price_cents)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    batch_id,
                    customer_id,
                    screening_id,
                    screening["room_id"],
                    seat_id,
                    screening["ticket_price_cents"],
                ),
            )
            reservation_ids.append(cursor.lastrowid)
        db.commit()
        return batch_id, reservation_ids
    except Exception:
        db.rollback()
        raise


def get_schedule(day):
    db = get_db()
    rows = db.execute(
        """SELECT screenings.*, films.title AS film_title, films.is_national,
                  rooms.name AS room_name
        FROM screenings
        JOIN films ON films.id = screenings.film_id
        JOIN rooms ON rooms.id = screenings.room_id
        WHERE date(screenings.starts_at) = date(?)
        ORDER BY screenings.starts_at""",
        (day,),
    ).fetchall()
    return rows, any(row["is_national"] for row in rows)
