# -*- coding: utf-8 -*-
"""
    MARE-app
"""

from __future__ import with_statement
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, jsonify
from werkzeug import check_password_hash, generate_password_hash


import os
import sys
import time

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,here)

from mare.config import Config
from mare.extensions import SQLAlchemy
from mare.extensions import mail
from mare.extensions import sendmail
from mare.views.accounts import accounts

#from flaskext.sqlalchemy import SQLAlchemy


def setup_mail_handler():

    import logging
    from logging import Formatter
    from logging.handlers import SMTPHandler

    ADMINS = ['stuart.powers@gmail.com']
    mail_handler = SMTPHandler('smtp.gmail.com', 'mare.mailer@gmail.com', ADMINS, 'New Video Uploaded',('mare.mailer','marepasstown',),secure=())
    mail_handler.setLevel(logging.DEBUG)

    mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s
        Message:

        %(message)s
        '''))

    return mail_handler


def create_app(name):

    app = Flask(name)
    app.config.from_object(Config)

    app.register_blueprint(accounts)

    db = SQLAlchemy()
    db.init_app(app)
    mail.init_app(app)

    app.logger.addHandler(setup_mail_handler())

    return app
