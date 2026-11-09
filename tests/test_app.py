import re

import pytest

from cine_senac import create_app, create_account


@pytest.fixture
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(tmp_path / "cine-senac.sqlite"),
            "COOKIE_SECURE": False,
        }
    )
    with application.app_context():
        create_account("admin", "admin-password", "admin")
        create_account("gestor", "gestor-password", "manager")
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


def csrf_token(response):
    match = re.search(rb'name="csrf_token" value="([^"]+)"', response.data)
    assert match, "A página deve incluir um token CSRF nos formulários."
    return match.group(1).decode()


def post_form(client, page, action, values):
    page_response = client.get(page)
    assert page_response.status_code == 200
    return client.post(
        action,
        data={"csrf_token": csrf_token(page_response), **values},
        follow_redirects=True,
    )


def sign_in(client, username="gestor", password="gestor-password"):
    response = post_form(
        client,
        "/entrar",
        "/entrar",
        {"username": username, "password": password},
    )
    assert response.status_code == 200
    return response


def create_room(client, name="Sala 1", seats=3):
    return post_form(
        client,
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


def create_film(client, title="Filme nacional", national="on"):
    return post_form(
        client,
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
            "nacional": national,
        },
    )


def create_session(client, start, title="Filme nacional"):
    response = post_form(
        client,
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
    assert response.status_code == 200
    assert title.encode() in response.data or b"Sess" in response.data
    return response


def register_customer(client, email="cliente@example.test"):
    return post_form(
        client,
        "/cadastro",
        "/cadastro",
        {
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
        },
    )


def reserve_seats(client, session_id, seat_ids):
    review_page = client.get(f"/sessoes/{session_id}/assentos")
    assert review_page.status_code == 200
    return client.post(
        f"/reservas/revisar/{session_id}",
        data={
            "csrf_token": csrf_token(review_page),
            "assento_ids": [str(seat_id) for seat_id in seat_ids],
        },
        follow_redirects=True,
    )


def confirm_reservation(client):
    page = client.get("/reservas/revisar")
    assert page.status_code == 200
    return client.post(
        "/reservas/confirmar",
        data={"csrf_token": csrf_token(page)},
        follow_redirects=True,
    )


def prepare_catalog(client):
    sign_in(client)
    create_room(client)
    create_film(client)
    create_session(client, "2026-12-01T10:00")


def test_home_page_renders_catalog_with_jinja(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"CineSenac" in response.data
    assert b"Filmes" in response.data


def test_manager_can_create_room_film_and_national_session(client):
    sign_in(client)
    room_response = create_room(client)
    film_response = create_film(client)
    session_response = create_session(client, "2026-12-01T10:00")

    assert b"Sala cadastrada" in room_response.data
    assert b"Filme cadastrado" in film_response.data
    assert b"Sess" in session_response.data

    schedule = client.get("/gestao/programacao?dia=2026-12-01")
    assert schedule.status_code == 200
    assert "2026-12-01".encode() in schedule.data
    assert b"Filme nacional" in schedule.data


def test_manager_routes_require_server_side_role_authorization(client):
    response = client.get("/gestao/salas/nova")
    assert response.status_code == 302

    sign_in(client, "admin", "admin-password")
    assert client.get("/gestao/salas/nova").status_code == 200
    assert client.get("/gestao/cadastros/clientes").status_code == 200


def test_manager_can_consult_rooms_films_and_screenings(client):
    sign_in(client)
    create_room(client)
    create_film(client)
    create_session(client, "2026-12-01T10:00")

    for kind, expected in (
        ("salas", "Sala 1"),
        ("filmes", "Filme nacional"),
        ("sessoes", "Filme nacional"),
    ):
        response = client.get(f"/gestao/cadastros/{kind}")
        assert response.status_code == 200
        assert expected.encode() in response.data


def test_manager_cannot_read_customer_personal_data(client):
    sign_in(client)

    response = client.get("/gestao/cadastros/clientes")

    assert response.status_code == 403


def test_customer_email_is_unique(client):
    first = register_customer(client)
    assert b"Cadastro realizado" in first.data

    post_form(client, "/", "/sair", {})
    duplicate = register_customer(client)

    assert b"e-mail j\xc3\xa1 cadastrado" in duplicate.data.lower()
    assert b'value="Cliente de Teste"' in duplicate.data


def test_customer_can_review_and_confirm_multiple_seats(client):
    prepare_catalog(client)
    register_customer(client)
    seats_page = client.get("/sessoes/1/assentos")
    assert b"assento_ids" in seats_page.data
    seat_ids = re.findall(rb'name="assento_ids" value="(\d+)"', seats_page.data)
    assert len(seat_ids) == 3

    review = reserve_seats(client, 1, [int(seat_ids[0]), int(seat_ids[1])])
    assert b"Revise sua reserva" in review.data
    assert b"Cliente de Teste" in review.data

    confirmation = confirm_reservation(client)
    assert b"Reserva confirmada" in confirmation.data
    assert b"2 assento" in confirmation.data


def test_customer_cannot_reserve_same_seat_twice(client):
    prepare_catalog(client)
    register_customer(client, "primeiro@example.test")
    seat_ids = re.findall(
        rb'name="assento_ids" value="(\d+)"',
        client.get("/sessoes/1/assentos").data,
    )
    reserve_seats(client, 1, [int(seat_ids[0])])
    assert b"Reserva confirmada" in confirm_reservation(client).data

    post_form(client, "/", "/sair", {})
    register_customer(client, "segundo@example.test")
    conflict = reserve_seats(client, 1, [int(seat_ids[0])])

    assert "disponíveis" in conflict.data.decode().lower()


def test_customer_cannot_confirm_conflicting_sessions(client):
    sign_in(client)
    create_room(client, seats=4)
    create_film(client)
    create_session(client, "2026-12-01T10:00")
    create_session(client, "2026-12-01T10:30")
    register_customer(client)

    first_seat = re.findall(
        rb'name="assento_ids" value="(\d+)"',
        client.get("/sessoes/1/assentos").data,
    )[0]
    reserve_seats(client, 1, [int(first_seat)])
    assert b"Reserva confirmada" in confirm_reservation(client).data

    second_seat = re.findall(
        rb'name="assento_ids" value="(\d+)"',
        client.get("/sessoes/2/assentos").data,
    )[0]
    review = reserve_seats(client, 2, [int(second_seat)])
    result = confirm_reservation(client)

    assert b"conflit" in result.data.lower(), result.data.decode()


def test_posts_without_csrf_token_are_rejected(client):
    response = client.post("/entrar", data={"username": "gestor"})

    assert response.status_code == 400
