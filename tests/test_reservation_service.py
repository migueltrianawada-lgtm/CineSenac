import sqlite3

import pytest

from cine_senac import create_app
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


@pytest.fixture
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(tmp_path / "reservations.sqlite"),
            "COOKIE_SECURE": False,
        }
    )


def customer_data(email):
    return {
        "nome": "Cliente",
        "idade": "30",
        "email": email,
        "logradouro": "Rua Central",
        "numero": "10",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000",
    }


def test_multi_seat_confirmation_is_atomic_and_idempotent(app):
    with app.app_context():
        room_id = create_room(
            {
                "nome": "Sala",
                "quantidade_assentos": "3",
                "horario_abertura": "09:00",
                "horario_fechamento": "23:00",
                "especificacao_tecnica": "Projeção digital",
            }
        )
        film_id = create_film(
            {
                "titulo": "Filme",
                "duracao_minutos": "90",
                "genero": "Drama",
                "sinopse": "Sinopse",
                "cartaz_url": "https://example.test/poster.jpg",
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
        first_customer = create_customer(customer_data("first@example.test"))
        second_customer = create_customer(customer_data("second@example.test"))
        seat_ids = [
            row["id"]
            for row in get_db()
            .execute("SELECT id FROM seats WHERE room_id = ? ORDER BY id", (room_id,))
            .fetchall()
        ]

        original_batch, original_reservations = confirm_reservation(
            screening_id,
            first_customer,
            [seat_ids[0]],
            "first-request",
        )
        retried_batch, retried_reservations = confirm_reservation(
            screening_id,
            first_customer,
            [seat_ids[0]],
            "first-request",
        )

        assert (retried_batch, retried_reservations) == (
            original_batch,
            original_reservations,
        )

        with pytest.raises(ReservationConflict):
            confirm_reservation(
                screening_id,
                first_customer,
                [seat_ids[1]],
                "first-request",
            )

        with pytest.raises(sqlite3.IntegrityError):
            confirm_reservation(
                screening_id,
                second_customer,
                [seat_ids[0], seat_ids[1]],
                "second-request",
            )

        assert get_db().execute(
            "SELECT count(*) FROM reservations WHERE customer_id = ?",
            (second_customer,),
        ).fetchone()[0] == 0
        assert seat_ids[1] in {row["id"] for row in available_seats(screening_id)}
