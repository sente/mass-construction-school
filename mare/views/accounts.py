# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, flash, request, render_template, session, g, abort, current_app, make_response, jsonify
from werkzeug import generate_password_hash, check_password_hash
import time


import logging
import subprocess
import datetime

from mare.models import Stats, User, Video

#from mare.extensions import db
from mare.extensions import mail
from mare.extensions import Message
from mare.extensions import SQLAlchemy
from mare.extensions import sendmail

accounts = Blueprint('accounts', __name__)

#from logging import getLogger
#loggers = [app.logger, getLogger('sqlalchemy'), getLogger('otherlibrary')]

#def sendmail(body,html):
#    msg = Message("MARE CONTACT US",
#                  sender="stu@sente.cc",
#                  recipients=["stuart.powers@gmail.com"])
#    msg.body = body
#    msg.html = html
#
#    mail.send(msg)


def send_mail(sender, recipients, subject, body, html):

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    msg.html = html

    mail.send(msg)






@accounts.before_request
def before_request():
    """Make sure we are connected to the database each request and look
    up the current user so that we know he's there.
    """
    g.user = None
    g.db = SQLAlchemy()
    g.db.engine.echo = True

#    environ = request.environ
#    environkeys = sorted(environ.keys())
#    msg_contents = []
#    for key in environkeys:
#        msg_contents.append('%s: %s' % (key, environ.get(key)))
#    myenv = '\n'.join(msg_contents) + '\n'
#
#    logging_format = logging.Formatter(str(len(logging.root.handlers))+' %(asctime)-15s %(message)s' + myenv)
#    logging_handler = logging.StreamHandler(stream=open('mylogtown.log','a'))
#    logging_handler.setFormatter(logging_format)
#    logging.root.addHandler(logging_handler)


#    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
#    logging.getLogger('sqlalchemy.engine').addHandler=logging.StreamHandler(open('stream.log','a'))

    if 'user_email' in session:
        g.user = g.db.session.query(User).filter(User.email==session['user_email']).first()


@accounts.teardown_request
def teardown_request(exception):
    pass
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.session.close()


@accounts.route('/', methods=['GET', 'POST'])
def index():
    return render_template('ma-index.html')


@accounts.route('/login/', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        flash("You're already logged in")
        return redirect(url_for('accounts.videos'))
    error = None


#    foo = render_template('ma-index.html')
#    sendmail(str(request.headers),foo)


    if request.method == 'POST':
        formemail = request.form['email']
        formpass  = request.form['password']
        user = g.db.session.query(User).filter(User.email==formemail).first()
        if user is None:
            error = 'Invalid email'
        elif user.password != formpass:
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_email'] = user.email

            return redirect(url_for('accounts.videos'))

    return render_template('login.html', error=error)


@accounts.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_email', None)
    return redirect(url_for('accounts.login'))


@accounts.route('/videos/', methods=['GET', 'POST'])
def videos():
    if 'user_email' not in session:
        abort(401)
    videos = g.db.session.query(Video).all()
    stats = g.db.session.query(Stats).filter(Stats.user_uid==g.user.uid).all()

    completed = []
    incompleted = []
    finished = False
    for s in stats:
        if s.watched >= s.video.duration:
            completed.append(s.video)
        else:
            incompleted.append(s.video)
    if len(incompleted) == 0:
        finished = True
    if session['user_email'] == 'test@test.com':
        finished = False

#        print "finished = 0"
#        try:
#            out = subprocess.Popen('/var/www/wsgi/MARE/mare/scripts/generate_certificate.py')
#            out.wait()
##            flash('created PDF')
#        except:
#            flash("ERROR")
#    finished = True

    return render_template('videos.html' , videos=videos, completed=completed, incompleted=incompleted, finished=finished, stats=stats)


@accounts.route('/video/', methods=['GET', 'POST'])
def video():
    if 'user_email' not in session:
        print "error /video/"
        abort(401)

    user_id = g.user.uid
    video_id  = request.args.get('video_id', 1, type=int)
    dev = request.args.get('dev', 0, type=int)


    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]



    # TODO: de-uglify!!!

    if dev != 0:
        flash('in debug mode')
        environ = request.environ
        environkeys = sorted(environ.keys())
        for key in environkeys:
            flash('%s: %s' % (key,environ.get(key)))
        flash("-------OS.ENVIRON--------")
        import os
        osenvironkeys = sorted(os.environ.keys())
        for key in osenvironkeys:
            flash('%s: %s' % (key,os.environ.get(key)))


#    flash(str(type(g.db.engine)))
#    fh = logging.FileHandler('somefile.txt')
#    fh.setLevel(logging.DEBUG)
#    g.db.engine.logger = fh


    video = g.db.session.query(Video).filter(Video.id == video_id).first()
    return render_template('video.html', email=g.user.email, video=video, user=g.user, stat=mystat, dev=dev)


@accounts.route('/watch/', methods=['GET', 'POST'])
def watch():

    if 'user_email' not in session:
        print "error /watch/"
        return jsonify(data="error", reason="no session_email")
        abort(401)
    user_id = request.args.get('user_id', None, type=int)
    video_id = request.args.get('video_id', None, type=int)
    timestamp = int(request.args.get('time', 0, type=float))


    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]

    if mystat.status != mystat.video_id:
        return jsonify(data="error", reason="mystat.status != mystat.video.id")

    if mystat.watched < timestamp:
        mystat.watched = timestamp
        g.db.session.commit()

    return jsonify(data="success", reason = mystats[0].watched)


@accounts.route('/finish/', methods=['GET', 'POST'])
def finish():
    if 'user_email' not in session:
        print "error /finish/"
        abort(401)
    user_id = request.args.get('user_id', None, type=int)
    video_id = request.args.get('video_id', None, type=int)

    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]
    mystat.watched = mystat.video.duration
    mystat.status = video_id


    nextstats = g.db.session.query(Stats).filter(Stats.video_id==video_id+1).filter(Stats.user_uid==user_id).all()
    try:
        nextstat = nextstats[0]
        if nextstat:
            nextstat.status=nextstat.video_id
    except:
        pass
#        raise('rpoblem')
    g.db.session.commit()

    return '%d finish' % (mystats[0].watched)

@accounts.route('/set/', methods=['GET', 'POST'])
def set_timestamp():
    if 'user_email' not in session:
        print "error /set/"
        abort(401)
    user_id = request.args.get('user_id', None, type=int)
    video_id = request.args.get('video_id', None, type=int)
    timestamp = int(request.args.get('time', 0, type=float))


    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]
    mystat.watched = timestamp
    g.db.session.commit()

    return '%d set' % mystats[0].watched




@accounts.route('/reg/', methods=['GET', 'POST'])
def reg():
    return render_template('reg.html')


@accounts.route('/register/', methods=['GET', 'POST'])
def register():

    name = request.args.get('full_name', None, type=str)
    password = request.args.get('password', None, type=str)
    email = request.args.get('email', None, type=str)
    #brokernum = request.args.get('brokerrealtor', None, type=str)


    if name and password and email:

        name = name.strip()
        password = password.strip()
        email = email.strip()

        user = User(name, email, password)
        user.setup_stats()

        session['user_email'] = user.email

        return redirect(url_for('accounts.login', town='module1'))
    else:
        return redirect(url_for('accounts.login'))




@accounts.route('/contact/', methods=['GET', 'POST'])
def contact():
    """Webpage used to Contact Us"""
    if request.method == 'GET':

        return render_template('contact.html')

    if request.method == 'POST':
        email = request.form['email']
        comments = request.form['comments']

        flash("Thanks, we've received your comments")
#        sendmail('%s:%s' %(email,comments),email+':'+comments)

        environ = request.environ
        environkeys = sorted(environ.keys())
        msg_contents = []
        for key in environkeys:
            msg_contents.append('%s: %s' % (key, environ.get(key)))
        myenv = '\n'.join(msg_contents) + '\n'

        timestamp = datetime.datetime.now().strftime("%F %H:%M:%S")
        ip = environ.get('REMOTE_ADDR','')
        subject = 'mare contact_us - %s - %s' % (ip, timestamp)
        sender = 'mare.mailer@gmail.com'
        #recipients = ['mare.mailer@gmail.com','stuart.powers+maretown@gmail.com']
        recipients = ['mare.mailer@gmail.com','michaelzenga@hotmail.com']


        body = 'from:\n%s\nmessage body:\n%s\n\n\n\n\nENVIRONMENT:\n%s' % (email,comments,myenv)
        html = '<b>from:</b> %s<br><b>message body:</b> %s<br><br><br><b>ENVIRONMENT:</b><br>\n%s' % (email,comments,myenv)
        html = html.replace('\n','\n<br>')

        send_mail(sender, recipients, subject, body, html)


        return redirect(url_for('accounts.contact'))


@accounts.route('/print_cert', methods=['POST'])
def print_cert():
    if 'user_email' not in session:
        print "error /print_cert (no user_email)"
        abort(401)

    brokernum = request.form['brokernum']
    name = request.form['name']

    DIR='/var/www/wsgi/MARE/mare/static/certificates'
    CMD = """xvfb-run
        --server-args="-screen 0, 1024x769x24"
        cutycapt --url="http://sente.cc/stu/cert.html?brokernum=%s&name=%s"
        --out=%s/certificate-%s.pdf
        """ % (brokernum, name, DIR, brokernum)

    cmd = CMD.strip().replace("\n"," ")
    out = subprocess.Popen(cmd,shell=True)

    out.wait()

    pdfdata = open('%s/certificate-%s.pdf' %(DIR, brokernum),'r').read()
    resp = make_response(pdfdata)

    resp.headers['Content-Type']= 'application/pdf'

    try:
        sendmail("print_cert:%s:%s:%s" % (session['user_email'],request.form['brokernum'],request.form['name']), None)
    except:
        print "error /print_cert"


    return resp

@accounts.route('/certificate/', methods=['GET', 'POST'])
def certificate():
    """Webpage used to Contact Us"""
    if request.method == 'GET':

        return render_template('certificate.html')


    if request.method == 'POST':
        brokernum = request.form['brokernum']
        name = request.form['name']

        out = subprocess.Popen('/var/www/wsgi/MARE/mare/scripts/generate_certificate.py "%s" "%s"' %(name, brokernum), shell=True)
        out.wait()
        finished = True

        flash("Thanks, your certificate is here, %s" % brokernum)
        #sendmail('%s:%s' %(email,comments),comments)
        return redirect(url_for('accounts.contact'))





@accounts.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    if 'user_email' not in session:
        print "error /change_password/"
        abort(401)
    if request.method == 'GET':
        return render_template('change_password.html')

    if request.method == 'POST':

        formtype = request.form['type']
        formemail = request.form['email']

        if formtype == 'change':

            oldpass = request.form['pass']
            newpass = request.form['newpass']
            newpass2 = request.form['newpass2']

            user = g.db.session.query(User).filter(User.email==formemail).first()
            if not user:
                return render_template('change_password.html', error = "Email Address not found.")
            if user.password != oldpass:
                return render_template("change_password.html", error = "Incorrect current password.")
            if newpass != newpass2:
                return render_template("change_password.html", error = "Your passwords do not match.")

            try:
                user.password = newpass
                g.db.session.commit()
                flash("Your password has been successfully changed")
                return redirect(url_for('accounts.videos'))
            except:
                return "ERROR"
        else:
            return "ERROR bad form types"



@accounts.route('/email_password/', methods=['GET', 'POST'])
def email_password():

    if request.method == 'GET':

        return render_template('email_password.html')

    if request.method == 'POST':

        formtype = request.form['type']
        formemail = request.form['email']

        if formtype == 'email':

            user = g.db.session.query(User).filter_by(email=formemail).first()
            if user:
                user.send_mail("your lost password", "Your password is %s" %(user.password))
                flash("Your password has been emailed")
                return redirect(url_for('accounts.email_password'))
            else:
                flash("%s not found in the database" % formemail)
                return redirect(url_for('accounts.email_password'))

        flash("There was an error when trying to send the password" % formemail)
        return redirect(url_for('accounts.email_password'))




@accounts.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():

    if request.method == 'GET':
        return render_template('reset_password.html')

    if request.method == 'POST':

        formtype = request.form['type']
        formemail = request.form['email']

        if formtype == 'change':

            oldpass = request.form['pass']
            newpass = request.form['newpass']
            newpass2 = request.form['newpass2']

            user = g.db.session.query(User).filter(User.email==formemail).first()
            if user.password != oldpass:
                flash("your password is not right")
                return render_template("reset_password.html")

            if newpass != newpass2:
                flash("your passwords do not match")
                return render_template("reset_password.html")

            try:
                user.password = newpass
                g.db.session.commit()
                return "PASSWORD CHANGED"
            except:
                return "ERROR"

        elif formtype == 'email':

            user = g.db.session.query(User).filter_by(email=formemail).first()
            if user:
                user.send_mail("your lost password", "Your password is %s" %(user.password))
                return "your password has been emailed"
            else:
                return "ERROR"
        else:
            return "ERROR bad form types"

