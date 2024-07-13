import logging
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import SQLAlchemyError

from database.populate import populate_db_with_data
from database.db import db

from .config import Config


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)
    app.logger.setLevel(logging.DEBUG)
    JWTManager(app)

    app.logger.debug("initializing db..")
    try:
        db.init_app(app)
    except SQLAlchemyError as e:
        app.logger.error(e)
        raise e

    with app.app_context():
        # importing routes to register them in another file
        # pylint: disable=import-outside-toplevel,unused-import
        from . import routes  # noqa: F401
        try:
            # only for the assignment to make sure no residues from last run
            db.drop_all()
            app.logger.debug("db cleared")
            db.create_all()
            app.logger.debug("db tables created")
            app.logger.debug("populating db with data..")
            populate_db_with_data(db)
            app.logger.debug("db populated with data")
        except SQLAlchemyError as e:
            app.logger.error(e)
            raise e

    return app
