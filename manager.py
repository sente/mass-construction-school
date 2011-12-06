
from flask import current_app
from flaskext.script import Manager, prompt_bool
from mare import create_app

from mare.extensions import db
from mare.models import User, Video, Parent, Child, Stats

app = create_app('mare')
manager = Manager(app)


@manager.command
def create_user(name, brokernum, email, password):
    """
    Will create a user from supplied cli arguments.
    Since 'create_user' knows to check for an existing user first
    this will not create more than one of the same users.
    """

    try:
        user = User(name, brokernum, email, password)
        db.session.add(user)
        db.session.commit()
    except Exception, e:
        print e




@manager.command
def create_db():
    db.create_all()
    db.session.commit()





@manager.command
def drop_db():
    if prompt_bool('Are you sure you want to destroy all your data?'):
        db.drop_all()




@manager.command
def load_videos():
    with open('mare/data/videos_final.dat', 'r') as f:
        for line in f.readlines():
            tup = line.strip().split("\t")
            module = tup[0]
            duration = int(tup[1])
            title = tup[2]

            v = Video()
            v.module = module
            v.duration = duration
            v.title = title

            db.session.add(v)
            db.session.commit()



@manager.command
def full_test():
    db.drop_all()
    db.create_all()
    load_videos()
    stuart = User('Stuart Powers',12345,'stuart.powers@gmail.com','test')
    db.session.add(stuart)
    db.session.commit()

    videos = db.session.query(Video).all()
    for v in videos:
        s=Stats(stuart,v)
        db.session.add(s)
        db.session.commit()



@manager.shell
def make_shell_context():
    return dict(
        app=current_app,
        db=db,
        User=User,
        Video=Video,
        Parent=Parent,
        Child=Child,
        Stats=Stats
    )

if __name__ == "__main__":
    manager.run()

