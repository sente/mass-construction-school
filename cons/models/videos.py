from cons.extensions import db

class Video(db.Model):

    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.String(250))
    duration = db.Column(db.Integer)
    title = db.Column(db.String(250))

