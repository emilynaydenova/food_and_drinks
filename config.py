# use python-decouple
from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestApplicationConfig:
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config_app='config.DevelopmentConfig'):
    # this WSGI app is an instance of class Flask
    app = Flask(__name__)

    # configuring flask app and db connection string
    app.config.from_object(config_app)

    # api wraps app, makes it a Restful API
    api = Api(app)

    # allow changing column type
    migrate = Migrate(compare_type=True)
    migrate.init_app(app, db)

    # Initializes Cross Origin Resource sharing for the application
    CORS(app)

    # Adding resources for endpoints in routes.py
    [api.add_resource(*r) for r in routes]

    return app
