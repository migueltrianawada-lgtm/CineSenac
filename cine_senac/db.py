import sqlite3

import click
from flask import current_app, g


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'manager'))
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    seat_count INTEGER NOT NULL CHECK (seat_count > 0),
    opening_time TEXT NOT NULL,
    closing_time TEXT NOT NULL,
    technical_specification TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS films (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    genre TEXT NOT NULL,
    synopsis TEXT NOT NULL,
    poster_url TEXT NOT NULL,
    rating TEXT NOT NULL,
    cast_description TEXT NOT NULL,
    is_national INTEGER NOT NULL DEFAULT 0 CHECK (is_national IN (0, 1))
);

CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    UNIQUE (room_id, label),
    UNIQUE (id, room_id)
);

CREATE TABLE IF NOT EXISTS screenings (
    id INTEGER PRIMARY KEY,
    film_id INTEGER NOT NULL REFERENCES films(id),
    room_id INTEGER NOT NULL REFERENCES rooms(id),
    starts_at TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    ticket_price_cents INTEGER NOT NULL CHECK (ticket_price_cents >= 0),
    UNIQUE (id, room_id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 0),
    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
    street TEXT NOT NULL,
    number TEXT NOT NULL,
    complement TEXT NOT NULL DEFAULT '',
    neighborhood TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reservation_batches (
    id INTEGER PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    request_hash TEXT NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    screening_id INTEGER NOT NULL REFERENCES screenings(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY,
    batch_id INTEGER NOT NULL REFERENCES reservation_batches(id),
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    screening_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    seat_id INTEGER NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (screening_id, seat_id),
    FOREIGN KEY (screening_id, room_id) REFERENCES screenings(id, room_id),
    FOREIGN KEY (seat_id, room_id) REFERENCES seats(id, room_id)
);

CREATE INDEX IF NOT EXISTS idx_screenings_starts_at ON screenings(starts_at);
CREATE INDEX IF NOT EXISTS idx_reservations_customer ON reservations(customer_id);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            timeout=10,
            isolation_level=None,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA busy_timeout = 10000")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Base inicializada.")
