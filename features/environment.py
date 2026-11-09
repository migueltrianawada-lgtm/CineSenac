import tempfile
from pathlib import Path

from cine_senac import create_account, create_app


def before_scenario(context, _scenario):
    context.tempdir = tempfile.TemporaryDirectory()
    context.app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "DATABASE": str(Path(context.tempdir.name) / "cine-senac.sqlite"),
            "COOKIE_SECURE": False,
        }
    )
    context.client = context.app.test_client()
    with context.app.app_context():
        create_account("admin", "admin-password", "admin")
        create_account("gestor", "gestor-password", "manager")
    context.last_response = None


def after_scenario(context, _scenario):
    app_context = getattr(context, "app_context", None)
    if app_context is not None:
        app_context.pop()
    context.tempdir.cleanup()
