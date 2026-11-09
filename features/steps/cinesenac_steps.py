import re
import sqlite3

from behave import given, then, when

from cine_senac import create_account, create_app
from cine_senac.db import get_db
from cine_senac.services import (
    ReservationConflict,
    available_seats,
    confirm_reservation,
    create_customer,
    create_film,
    create_room,
    create_screening,
)


MANAGER_PASSWORD = "gestor-password"
ADMIN_PASSWORD = "admin-password"


def csrf_token(response):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match, "A página deve incluir um token CSRF nos formulários."
    return match.group(1).decode()


def post_form(context, page, action, values):
    response = context.client.get(page)
    assert response.status_code == 200
    return context.client.post(
        action,
        data={"csrf_token": csrf_token(response), **values},
        follow_redirects=True,
    )


def sign_in(context, username="gestor", password=MANAGER_PASSWORD):
    return post_form(
        context,
        "/entrar",
        "/entrar",
        {"username": username, "password": password},
    )


def create_room_web(context, name="Sala 1", seats=3):
    return post_form(
        context,
        "/gestao/salas/nova",
        "/gestao/salas/nova",
        {
            "nome": name,
            "quantidade_assentos": str(seats),
            "horario_abertura": "09:00",
            "horario_fechamento": "23:00",
            "especificacao_tecnica": "Projeção digital",
        },
    )


def create_film_web(context, title="Filme nacional"):
    return post_form(
        context,
        "/gestao/filmes/novo",
        "/gestao/filmes/novo",
        {
            "titulo": title,
            "duracao_minutos": "100",
            "genero": "Drama",
            "sinopse": "Uma história de cinema.",
            "cartaz_url": "https://example.test/cartaz.jpg",
            "faixa_etaria": "Livre",
            "elenco": "Elenco de teste",
            "nacional": "on",
        },
    )


def create_screening_web(context, start):
    return post_form(
        context,
        "/gestao/sessoes/nova",
        "/gestao/sessoes/nova",
        {
            "filme_id": "1",
            "sala_id": "1",
            "inicio": start,
            "duracao_minutos": "100",
            "valor_ingresso": "25.50",
        },
    )


def customer_data(email):
    return {
        "nome": "Cliente de Teste",
        "idade": "30",
        "email": email,
        "logradouro": "Rua Central",
        "numero": "10",
        "complemento": "",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000",
    }


def register_customer_web(context, email="cliente@example.test"):
    return post_form(context, "/cadastro", "/cadastro", customer_data(email))


def seat_ids_from_page(response):
    return [
        int(value)
        for value in re.findall(rb'name="assento_ids" value="(\d+)"', response.data)
    ]


def select_seats(context, screening_id, ids):
    page = context.client.get(f"/sessoes/{screening_id}/assentos")
    assert page.status_code == 200
    return context.client.post(
        f"/reservas/revisar/{screening_id}",
        data={
            "csrf_token": csrf_token(page),
            "assento_ids": [str(seat_id) for seat_id in ids],
        },
        follow_redirects=True,
    )


def confirm_web_reservation(context):
    page = context.client.get("/reservas/revisar")
    assert page.status_code == 200
    return context.client.post(
        "/reservas/confirmar",
        data={"csrf_token": csrf_token(page)},
        follow_redirects=True,
    )


def prepare_catalog_web(context, seat_count=3, starts_at="2026-12-01T10:00"):
    sign_in(context)
    create_room_web(context, seats=seat_count)
    create_film_web(context)
    create_screening_web(context, starts_at)


def prepare_service_catalog(context):
    room_id = create_room(
        {
            "nome": "Sala de teste",
            "quantidade_assentos": "3",
            "horario_abertura": "09:00",
            "horario_fechamento": "23:00",
            "especificacao_tecnica": "Projeção digital",
        }
    )
    film_id = create_film(
        {
            "titulo": "Filme de teste",
            "duracao_minutos": "90",
            "genero": "Drama",
            "sinopse": "Sinopse",
            "cartaz_url": "https://example.test/cartaz.jpg",
            "faixa_etaria": "Livre",
            "elenco": "Elenco",
            "nacional": "on",
        }
    )
    screening_id = create_screening(
        {
            "filme_id": str(film_id),
            "sala_id": str(room_id),
            "inicio": "2026-12-01T10:00",
            "duracao_minutos": "100",
            "valor_ingresso": "20.00",
        }
    )
    return room_id, screening_id


def register_service_customer(email):
    return create_customer(customer_data(email))


def enter_app_context(context):
    context.app_context = context.app.app_context()
    context.app_context.push()


def leave_app_context(context):
    context.app_context.pop()


@when("acesso a página inicial")
def step_home_page(context):
    context.last_response = context.client.get("/")


@then("a resposta deve ser bem-sucedida")
def step_response_success(context):
    assert context.last_response.status_code == 200


@then('devo ver "{text}"')
def step_should_see_text(context, text):
    assert text.encode() in context.last_response.data


@given("que entrei como gestor")
def step_manager_signed_in(context):
    context.last_response = sign_in(context)
    assert b"Acesso realizado" in context.last_response.data


@when('cadastro uma sala, um filme nacional e uma sessão para "{start}"')
def step_create_room_film_screening(context, start):
    context.room_response = create_room_web(context)
    context.film_response = create_film_web(context)
    context.screening_response = create_screening_web(context, start)


@then("os três cadastros devem ser confirmados")
def step_catalog_created(context):
    assert b"Sala cadastrada" in context.room_response.data
    assert b"Filme cadastrado" in context.film_response.data
    assert "Sessão cadastrada".encode() in context.screening_response.data


@then('a programação de "{day}" deve conter "{title}"')
def step_schedule_contains(context, day, title):
    response = context.client.get(f"/gestao/programacao?dia={day}")
    assert response.status_code == 200
    assert day.encode() in response.data
    assert title.encode() in response.data


@when("tento abrir o cadastro de salas sem autenticação")
def step_try_room_form_without_auth(context):
    context.last_response = context.client.get("/gestao/salas/nova")


@then("sou redirecionado para entrar")
def step_redirected_to_login(context):
    assert context.last_response.status_code == 302
    assert "/entrar" in context.last_response.headers["Location"]


@when("entro como administrador")
def step_admin_sign_in(context):
    context.last_response = sign_in(context, "admin", ADMIN_PASSWORD)


@then("posso abrir o cadastro de salas")
def step_admin_can_open_rooms(context):
    assert context.client.get("/gestao/salas/nova").status_code == 200


@then("posso consultar os cadastros de clientes")
def step_admin_can_list_customers(context):
    assert context.client.get("/gestao/cadastros/clientes").status_code == 200


@given('que cadastrei sala, filme nacional e sessão para "{start}"')
def step_catalog_prepared_for_listing(context, start):
    create_room_web(context)
    create_film_web(context)
    create_screening_web(context, start)


@when("consulto os cadastros de salas, filmes e sessões")
def step_consult_catalog_records(context):
    context.record_responses = {
        kind: context.client.get(f"/gestao/cadastros/{kind}")
        for kind in ("salas", "filmes", "sessoes")
    }


@then("cada cadastro deve exibir seus dados")
def step_catalog_records_displayed(context):
    expected = {
        "salas": "Sala 1",
        "filmes": "Filme nacional",
        "sessoes": "Filme nacional",
    }
    for kind, text in expected.items():
        response = context.record_responses[kind]
        assert response.status_code == 200
        assert text.encode() in response.data


@when("tento consultar os cadastros de clientes")
def step_try_customer_records(context):
    context.last_response = context.client.get("/gestao/cadastros/clientes")


@then("o acesso é negado")
def step_access_denied(context):
    assert context.last_response.status_code == 403


@when("envio o formulário de entrada sem token CSRF")
def step_post_without_csrf(context):
    context.last_response = context.client.post(
        "/entrar", data={"username": "gestor", "password": MANAGER_PASSWORD}
    )


@then("a requisição é rejeitada com código 400")
def step_bad_request(context):
    assert context.last_response.status_code == 400


@when('cadastro um cliente com o e-mail "{email}"')
def step_register_customer(context, email):
    context.last_response = register_customer_web(context, email)
    assert b"Cadastro realizado" in context.last_response.data


@when("encerro a sessão do cliente")
def step_logout_customer(context):
    context.last_response = post_form(context, "/", "/sair", {})


@when('tento cadastrar outro cliente com o e-mail "{email}"')
def step_register_duplicate_customer(context, email):
    context.last_response = register_customer_web(context, email)


@then("o cadastro duplicado deve ser rejeitado")
def step_duplicate_email_rejected(context):
    assert context.last_response.status_code == 400
    assert "e-mail já cadastrado".encode() in context.last_response.data.lower()


@then("os dados preenchidos devem continuar disponíveis no formulário")
def step_customer_form_preserves_values(context):
    assert b'value="Cliente de Teste"' in context.last_response.data


@given("que existe uma sessão com três assentos disponíveis")
def step_three_available_seats(context):
    prepare_catalog_web(context)


@given("que estou cadastrado como cliente")
def step_customer_registered(context):
    context.last_response = register_customer_web(context)
    assert b"Cadastro realizado" in context.last_response.data


@when("seleciono dois assentos da sessão")
def step_select_two_seats(context):
    context.seat_ids = seat_ids_from_page(
        context.client.get("/sessoes/1/assentos")
    )
    assert len(context.seat_ids) == 3
    context.last_response = select_seats(context, 1, context.seat_ids[:2])


@then("a revisão deve exibir o cliente e a reserva")
def step_review_has_customer_and_booking(context):
    assert b"Revise sua reserva" in context.last_response.data
    assert b"Cliente de Teste" in context.last_response.data


@when("confirmo a reserva")
def step_confirm_reservation(context):
    context.last_response = confirm_web_reservation(context)


@then("a reserva deve ser confirmada para dois assentos")
def step_two_seats_confirmed(context):
    assert b"Reserva confirmada" in context.last_response.data
    assert b"2 assento" in context.last_response.data


@given("que um cliente já reservou um assento")
def step_first_customer_reserves_seat(context):
    register_customer_web(context, "primeiro@example.test")
    context.seat_ids = seat_ids_from_page(
        context.client.get("/sessoes/1/assentos")
    )
    select_seats(context, 1, [context.seat_ids[0]])
    assert b"Reserva confirmada" in confirm_web_reservation(context).data


@when("outro cliente tenta reservar o mesmo assento")
def step_second_customer_attempts_taken_seat(context):
    post_form(context, "/", "/sair", {})
    register_customer_web(context, "segundo@example.test")
    context.last_response = select_seats(context, 1, [context.seat_ids[0]])


@then("a seleção deve informar que o assento não está disponível")
def step_taken_seat_unavailable(context):
    assert "disponíveis" in context.last_response.data.decode().lower()


@given('que existem sessões às "{first_start}" e "{second_start}"')
def step_conflicting_screenings(context, first_start, second_start):
    sign_in(context)
    create_room_web(context, seats=4)
    create_film_web(context)
    create_screening_web(context, first_start)
    create_screening_web(context, second_start)


@when("confirmo uma reserva para a primeira sessão")
def step_reserve_first_screening(context):
    first_seat = seat_ids_from_page(
        context.client.get("/sessoes/1/assentos")
    )[0]
    select_seats(context, 1, [first_seat])
    context.first_confirmation = confirm_web_reservation(context)
    assert b"Reserva confirmada" in context.first_confirmation.data


@when("tento confirmar uma reserva para a segunda sessão")
def step_attempt_second_screening(context):
    second_seat = seat_ids_from_page(
        context.client.get("/sessoes/2/assentos")
    )[0]
    select_seats(context, 2, [second_seat])
    context.last_response = confirm_web_reservation(context)


@then("a segunda reserva deve ser rejeitada por conflito de horário")
def step_overlapping_screening_rejected(context):
    assert b"conflit" in context.last_response.data.lower()


@given("que existe uma sessão preparada para teste de confirmação")
def step_service_catalog_ready(context):
    enter_app_context(context)
    context.room_id, context.screening_id = prepare_service_catalog(context)
    context.first_customer_id = register_service_customer("first@example.test")
    context.second_customer_id = register_service_customer("second@example.test")
    context.service_seat_ids = [
        row["id"]
        for row in get_db()
        .execute(
            "SELECT id FROM seats WHERE room_id = ? ORDER BY id",
            (context.room_id,),
        )
        .fetchall()
    ]


@when("confirmo um assento e repito a mesma solicitação com a mesma chave")
def step_confirm_then_retry(context):
    context.original_confirmation = confirm_reservation(
        context.screening_id,
        context.first_customer_id,
        [context.service_seat_ids[0]],
        "first-request",
    )
    context.retried_confirmation = confirm_reservation(
        context.screening_id,
        context.first_customer_id,
        [context.service_seat_ids[0]],
        "first-request",
    )


@then("a repetição deve retornar a confirmação original")
def step_retry_is_idempotent(context):
    assert context.retried_confirmation == context.original_confirmation


@when("reutilizo a chave com uma solicitação diferente")
def step_reuse_key_with_different_request(context):
    try:
        confirm_reservation(
            context.screening_id,
            context.first_customer_id,
            [context.service_seat_ids[1]],
            "first-request",
        )
    except ReservationConflict as error:
        context.key_reuse_error = error
    else:
        raise AssertionError("A reutilização da chave deveria ser rejeitada.")


@then("a solicitação deve ser rejeitada por conflito de chave")
def step_key_reuse_rejected(context):
    assert "chave" in str(context.key_reuse_error).lower()


@when("outro cliente tenta reservar o assento ocupado e um assento livre")
def step_other_customer_reserves_taken_and_free_seats(context):
    try:
        confirm_reservation(
            context.screening_id,
            context.second_customer_id,
            context.service_seat_ids[:2],
            "second-request",
        )
    except sqlite3.IntegrityError as error:
        context.partial_reservation_error = error
    else:
        raise AssertionError("A reserva de assento ocupado deveria falhar.")


@then("a confirmação deve falhar sem reservar parcialmente os assentos")
def step_failed_confirmation_is_atomic(context):
    assert isinstance(context.partial_reservation_error, sqlite3.IntegrityError)
    assert (
        get_db()
        .execute(
            "SELECT count(*) FROM reservations WHERE customer_id = ?",
            (context.second_customer_id,),
        )
        .fetchone()[0]
        == 0
    )
    available_ids = {row["id"] for row in available_seats(context.screening_id)}
    assert context.service_seat_ids[1] in available_ids
