
from flask import current_app
from flaskext.script import Manager, prompt_bool
from mare import create_app

from mare.extensions import SQLAlchemy
from mare.models import User, Video, Stats

app = create_app('mare')
manager = Manager(app)

db = SQLAlchemy()


@manager.command
def create_user(name, email, password, brokernum=None):
    """
    Will create a user from supplied cli arguments.
    Since 'create_user' knows to check for an existing user first
    this will not create more than one of the same users.
    """

    try:
        user = User(name, email, password, brokernum)
        db.session.add(user)

        count = 0
        for v in db.session.query(Video).all():
            count += 1
            s = Stats(user, v)
            s.watched = 0
            if count == 1:
                s.status = 1
            else:
                s.status = 0
            db.session.add(s)

        db.session.commit()

    except Exception, e:
        print e




@manager.command
def create_db():
    db.create_all()
    #db.session.commit()





@manager.command
def drop_db():
    if prompt_bool('Are you sure you want to destroy all your data?'):
        db.drop_all()


@manager.command
def load_videos():
    with open('mare/data/videos.dat', 'r') as f:
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
    stuart = User('Stuart Powers', 'test@test.com', 'test', brokernum=None)
    db.session.add(stuart)
    db.session.commit()

    videos = db.session.query(Video).all()
    for v in videos:
        s=Stats(stuart,v)
        db.session.add(s)
        db.session.commit()

@manager.command
def run_stats():
    for u in db.session.query(User).all():
        ustats = db.session.query(Stats).filter_by(user=u).all()
        lastwatched = filter(lambda x:  x.status,ustats)
        if lastwatched:
            lastvid = sorted(lastwatched,key=lambda x: x.video.id)[-1]
            print "%d\t%d\t%d\t%s" % (lastvid.video.id,lastvid.watched,lastvid.user.uid,lastvid.user.email)
        else:
            print "100\t100\t%d\t%s" % (u.uid,u.email)






@manager.shell
def make_shell_context():
    return dict(
        app=current_app,
        db=db,
        User=User,
        Video=Video,
        Stats=Stats
    )

if __name__ == "__main__":
    manager.run()

