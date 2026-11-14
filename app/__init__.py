import click
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and set it.")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.auth import bp as auth_bp
    from app.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    register_commands(app)
    return app


def register_commands(app):
    from app.models import User

    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        db.create_all()
        click.echo("Database initialized.")

    @app.cli.command("create-user")
    @click.argument("email")
    @click.password_option()
    def create_user(email, password):
        """Create a user who can log in."""
        email = email.strip().lower()
        if db.session.scalar(db.select(User).filter_by(email=email)):
            click.echo(f"User {email} already exists.")
            return
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Created user {email}.")
