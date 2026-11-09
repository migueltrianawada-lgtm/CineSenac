import os
import secrets
from pathlib import Path

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from .db import close_db, get_db, init_db
from .web import register_routes


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.environ.get(
            "CINESENAC_DATABASE",
            str(Path(app.instance_path) / "cine-senac.sqlite"),
        ),
        SECRET_KEY=os.environ.get("CINESENAC_SECRET_KEY"),
        COOKIE_SECURE=os.environ.get("CINESENAC_COOKIE_SECURE", "false").lower()
        == "true",
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"]:
        if not app.testing and not app.debug:
            raise RuntimeError("CINESENAC_SECRET_KEY deve estar definida fora de testes.")
        app.config["SECRET_KEY"] = secrets.token_hex(32)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=app.config["COOKIE_SECURE"],
    )

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

    register_routes(app)

    @app.cli.command("create-account")
    @click.option("--username", prompt=True)
    @click.option("--role", type=click.Choice(["admin", "manager"]), prompt=True)
    @click.password_option()
    def create_account_command(username, role, password):
        create_account(username, password, role)
        click.echo(f"Conta {role} criada.")

    return app


def create_account(username, password, role):
    if role not in {"admin", "manager"}:
        raise ValueError("O perfil deve ser admin ou manager.")
    if len(password) < 12:
        raise ValueError("A senha deve ter ao menos 12 caracteres.")
    db = get_db()
    db.execute(
        "INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, ?)",
        (username.strip(), generate_password_hash(password), role),
    )
    db.commit()
