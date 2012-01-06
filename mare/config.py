# -*- encoding:utf-8 -*-

import os


this_directory = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    DEBUG = True #for devel

    SECRET_KEY = 'epoch-1323202600-town'
    #SQLAlchemy Settings

    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/dev.db' % this_directory
    SQLALCHEMY_RECORD_QUERIES = True


    CERTIFICATE_SCRIPT = "%s/scripts/generate_certificate.py" % this_directory
    CERTIFICATE_DIR  = "%s/static/certificates" % this_directory


    #WTForms Settings
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = '_csrf_token'

    #Flask Mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT =  25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = 'mare.mailer'
    DEFAULT_MAIL_SENDER = 'mare.mailer@gmail.com'

    if os.environ.has_key('MAREPASS'):
        MAIL_PASSWORD = os.environ['MAREPASS']
    MAIL_PASSWORD = 'marepasstown'

