# -*- encoding:utf-8 -*-

from flaskext.sqlalchemy import SQLAlchemy
from flaskext.mail import Mail
from flaskext.mail import Message

db = SQLAlchemy()
mail = Mail()



def sendmail(body,html):
    msg = Message("MARE CONTACT US",
                  sender="mare.mailer@gmail.com",
                  recipients=["mare.mailer@gmail.com"])
    msg.body = body
    msg.html = html

    mail.send(msg)

