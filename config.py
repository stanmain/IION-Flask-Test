# Copyright © 2018 Stanislav Hnatiuk. All rights reserved.

"""Module of configuration."""

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Class of configuration parameters."""

    JSON_AS_ASCII = False
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    CLIENT_PERIOD = 10
