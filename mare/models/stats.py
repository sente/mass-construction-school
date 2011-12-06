from mare.extensions import db


class Stats(db.Model):
    __tablename__ = 'stats'
    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    watched = db.Column(db.Integer)
    user = db.relationship("User")
    video = db.relationship("Video")

    def __init__(self, user, video):
        self.user = user
        self.video = video
        self.watched = 0

    def __repr__(self):
        return "<Stats('%r:%r:%d')>" % (self.user.name,self.video.module,self.watched)

class Parent(db.Model):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Child")


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
