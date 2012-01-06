from mare.extensions import db

class Stats(db.Model):

    __tablename__ = 'stats'

    uid = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    watched = db.Column(db.Integer)
    status = db.Column(db.Integer)
    user = db.relationship("User")
    video = db.relationship("Video")

    def __init__(self, user, video):
        self.user = user
        self.video = video
        self.status = 0
        self.watched = 0

    def __repr__(self):
        return "<Stats('%r:%r:%d')>" % (self.user.name, self.video.module, self.status, self.watched)

