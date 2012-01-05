import datetime
from mare.extensions import db, mail

from flaskext.sqlalchemy import BaseQuery
from flaskext.mail import Message
from werkzeug import generate_password_hash, check_password_hash

from mare.models.stats import Stats
from mare.models.videos import Video

class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    brokernum = db.Column(db.String)
#    active = db.Column(db.Boolean)
#    created = db.Column(db.DateTime)

    def __init__(self, name, brokernum, email, password):
        self.name = name
        self.brokernum = brokernum
        self.email = email
        self.password = password
        self.active = False
        self.created = datetime.datetime.utcnow()
#        self.pwdhash = generate_password_hash(password)


    def send_mail(self, subject, message):
        msg = Message( subject, recipients = [self.email], body = message)
        mail.send(msg)


    def setup_stats(self):
        count = 0
        for v in db.session.query(Video).all():
            count += 0
            s = Stats(self, v)
            s.watched = count
            db.session.add(s)
            db.session.commit()

    def get_stats(self,video=None):
        stats = db.session.query(Stats).filter_by(user=self)
        if video == None:
            return stats.all()
        if isinstance(video,(str)):
            return stats.filter(Stats.video.module==video).all()

        return stats


    def __repr__(self):
        return "<User('%d:%r')>" % (self.uid,self.email)

