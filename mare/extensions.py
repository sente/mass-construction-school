# -*- encoding:utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.mail import Message

db = SQLAlchemy()
mail = Mail()



def sendmail(body,html):
    msg = Message("MARE CONTACT US",
                  sender="massconstructionschool@gmail.com",
                  recipients=["massconstructionschool@gmail.com"])
    msg.body = body
    msg.html = html

    mail.send(msg)

