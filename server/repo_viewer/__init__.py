from flask import Flask
from flask_cors import CORS

import logging
from logging.handlers import SysLogHandler

import config
import sys


def create_app():
    from . import models, routes
    app = Flask(__name__)

    CORS(app, resources={r'/*': {'origins': '*'}})

    app.config.from_object(config)

    syslog_handler = None
    if sys.platform == 'darwin':
        syslog_handler = SysLogHandler(address='/var/run/syslog')
    elif sys.platform == 'linux':
        syslog_handler = SysLogHandler(address='/dev/log')

    if syslog_handler is not None:
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    app.logger.addHandler(stdout_handler)

    app.logger.setLevel(logging.INFO)

    app.logger.info('db = {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

    models.init_app(app)
    routes.init_app(app)
    return app
