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
from flask.ext import admin

import os
import sys
import time

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,here)

from cons.config import Config
from cons.extensions import SQLAlchemy
from cons.extensions import mail
from cons.extensions import sendmail
from cons.views.accounts import accounts
from cons.models import User, Video, Stats



def setup_mail_handler():

    import logging
    from logging import Formatter
    from logging.handlers import SMTPHandler

    ADMINS = ['stuart.powers@gmail.com']
    mail_handler = SMTPHandler('smtp.gmail.com', 'massconstructionschool@gmail.com', ADMINS, 'New Video Uploaded',('massconstructionschool@gmail.com',app.config['MAIL_PASSWORD'],))
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

def CreateLogger(name, logdir='', level=None):
    import logging
    import logging.handlers
    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG)
    if level != None:
        l.setLevel(level)

    epochtime = int(time.time())
    log_filename = os.path.join(logdir, "%s.%d.log" % (name, epochtime))
    handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=10240000, backupCount=10)
    formatter = logging.Formatter("%(asctime)s|%(thread)d|%(levelno)s|%(module)s:%(funcName)s:%(lineno)d|%(message)s")
    handler.setFormatter(formatter)
    l.addHandler(handler)
    return l


def create_app(name):

    app = Flask(name)
    app.config.from_object(Config)

    app.register_blueprint(accounts)

    db = SQLAlchemy()
    db.init_app(app)
    mail.init_app(app)

    app.logger.addHandler(CreateLogger('full', app.config['LOG_DIR']))

    return app
