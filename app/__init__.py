# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Package of application IION-Monitor."""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import Config


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):
    """Create app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.data import bp as data_bp
    app.register_blueprint(data_bp, url_prefix='/data')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        handler = RotatingFileHandler(
            'logs/microblog.log', maxBytes=10240, backupCount=10)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    app.logger.info('{} startup'.format(__name__))
    return app
