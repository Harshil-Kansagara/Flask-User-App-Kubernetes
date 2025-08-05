import os
import logging
from flask import Flask, jsonify, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config.config import config_by_name
from flasgger import Swagger

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """Application factory function.

    Args:
        config_name (str, optional): Configuration environment name. Defaults to None.

    Returns:
        Flask: Configured Flask application instance
    """

    app = Flask(__name__)
    Swagger(app)
    # Load configuration dynamically from config.py (which now loads from db_config.json)
    env = config_name or os.getenv("FLASK_ENV", "default")
    app.config.from_object(config_by_name[env])
    create_db(app)
    initialize_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    create_tables(app)

    logger.info("Flask application created successfully")
    return app


def create_db(app):
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    with app.app_context():  # Ensure app context for accessing config
        db_user = app.config["DB_USER"]
        db_password = app.config["DB_PASSWORD"]
        db_host = app.config["DB_HOST"]
        db_port = app.config["DB_PORT"]
        db_name = app.config["DB_NAME"]

    try:
        # Connect to the default database (postgres)
        conn = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE "{db_name}"')
            logger.info(f"Database '{db_name}' created successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to ensure database exists: {str(e)}")
        raise


def initialize_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    """Register application blueprints."""
    from app.routes.api import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    # Redirect root to Swagger UI
    @app.route("/")
    def root_redirect():
        return redirect("/apidocs")


def register_error_handlers(app):
    """Register global error handlers"""

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {"error": "Not Found", "message": "The required resource was not found"}
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                }
            ),
            500,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {
                    "error": "Bad Request",
                    "message": "The request could not be understood by the server",
                }
            ),
            404,
        )


def create_tables(app):
    with app.app_context():
        try:
            # Import models to ensure they're registered
            from app.models import user

            # Create all tables
            db.create_all()

            # Initialize sample data if needed
            from app.utils.db_helpers import initialize_sample_data

            initialize_sample_data()

            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise
