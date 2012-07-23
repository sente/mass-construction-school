import datetime
from cons.extensions import db, mail

from flask.ext.sqlalchemy import BaseQuery
from flask.ext.mail import Message
from werkzeug import generate_password_hash, check_password_hash

from cons.models.stats import Stats
from cons.models.videos import Video

class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    brokernum = db.Column(db.String)
    user_type = db.Column(db.Integer)

#    active = db.Column(db.Boolean)
#    created = db.Column(db.DateTime)

    def __init__(self, name, email, password, user_type, brokernum=None):
        self.name = name
        self.brokernum = brokernum
        self.email = email
        self.password = password
        self.user_type = user_type
        self.active = False
        self.created = datetime.datetime.utcnow()

#        self.pwdhash = generate_password_hash(password)


    def send_mail(self, subject, message):
        msg = Message(subject, recipients = [self.email], body=message, bcc=['cons.mailer@gmail.com'])
        mail.send(msg)


    def setup_stats(self):
        count = 0

        user_video_map = {99:6, 89:4, 69:2}

        num_videos = user_video_map.get(self.user_type, 6)

        for v in db.session.query(Video).order_by(Video.id).limit(num_videos).all():
            count += 1
            s = Stats(self, v)
            s.watched = 0
            if count == 1:
                s.status = 1
            else:
                s.status = 0
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

