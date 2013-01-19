# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, flash, request, render_template, session, g, abort, current_app, make_response, jsonify
from werkzeug import generate_password_hash, check_password_hash
import time

from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('accounts.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def log_path(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if g.user:
            user = g.user.email
        else:
            user = 'None'
        ip = request.environ.get('REMOTE_ADDR','None')
        url = request.url

        logstr = "%(ip)s:%(user)s:%(url)s" % { 'ip':ip, 'user':user, 'url':url }
        current_app.logger.info(logstr)

        return f(*args, **kwargs)
    return decorated_function

import logging
import subprocess
import datetime

from cons.models import Stats, User, Video

from cons.extensions import mail
from cons.extensions import Message
from cons.extensions import SQLAlchemy
from cons.extensions import sendmail

accounts = Blueprint('accounts', __name__)


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
    g.db.engine.echo = False

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

    contents = open('/srv/sftponly/shawn/massconstructionschool.com/ce/index.html','r').read()
    return contents
#    return render_template('ma-index.html')



@accounts.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Logs the user in.
    """
    if g.user:
        flash("You're already logged in")
        return redirect(url_for('accounts.videos'))
    error = None

    if request.method == 'POST':
        formemail = request.form['email']
        formpass  = request.form['password']
        current_app.logger.info('login:%s:%s' % (formemail, formpass))
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
    """
    Logs the user out.
    """
    flash('You were logged out')
    session.pop('user_email', None)
    return redirect(url_for('accounts.login'))


@accounts.route('/videos/', methods=['GET', 'POST'])
@log_path
def videos():
    """
    Listing page of all the videos and user progress
    """

    if 'user_email' not in session:
        flash('You have to sign in to view the videos')
        return redirect(url_for('accounts.login'))

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

    return render_template('videos.html' , videos=videos, completed=completed, incompleted=incompleted, finished=finished, stats=stats)


@accounts.route('/video/', methods=['GET', 'POST'])
@log_path
def video():
    """
    watch an individual video
    """

    if 'user_email' not in session:
        flash('You have to sign in to view the videos')
        return redirect(url_for('accounts.login'))

    user_id = g.user.uid
    video_id  = request.args.get('video_id', 1, type=int)
    dev = request.args.get('dev', 0, type=int)


    try:
        mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
        mystat = mystats[0]
    except:
        flash('Invalid request received')
        return redirect(url_for('accounts.videos'))


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

    video = g.db.session.query(Video).filter(Video.id == video_id).first()


#    flash(session['user_email'])
    if session['user_email'] == 'test@test.com':
        return render_template('video-flv.html', email=g.user.email, video=video, user=g.user, stat=mystat, dev=dev)
    return render_template('video.html', email=g.user.email, video=video, user=g.user, stat=mystat, dev=dev)


@accounts.route('/watch/', methods=['GET', 'POST'])
def watch():
    """
    called by javascript, this function updates the user's
    progress for the given video
    """

    if 'user_email' not in session:
        print "error /watch/"
        return jsonify(data="error", reason="no session_email")
        abort(401)
    user_id = request.args.get('user_id', None, type=int)
    video_id = request.args.get('video_id', None, type=int)
    timestamp = int(request.args.get('time', 0, type=float))

    try:
        current_app.logger.info('watch:%s:%d:%d:%f' % (session['user_email'],user_id,video_id,timestamp))
    except:
        pass

    try:
        mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
        mystat = mystats[0]
    except:
        current_app.logger.info('ERROR watch:%s:%d:%d:%f' % (session['user_email'],user_id,video_id,timestamp))
        return jsonify(data="error",reason="bad data")

    if mystat.status != mystat.video_id:
        return jsonify(data="error", reason="mystat.status != mystat.video.id")

    if mystat.watched < timestamp:
        mystat.watched = timestamp
        g.db.session.commit()

    return jsonify(data="success", reason = mystats[0].watched)


@accounts.route('/finish/', methods=['GET', 'POST'])
def finish():
    """
    called by javascript when the user has finished watching a video
    """

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

    g.db.session.commit()

    return '%d finish' % (mystats[0].watched)

@accounts.route('/set/', methods=['GET', 'POST'])
def set_timestamp():
    """
    this is a 'hidden' method that can be used to set a given user's video progress
    """
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
@log_path
def reg():
    """ renders the reg.html template """
    return render_template('reg.html')



@accounts.route('/register/', methods=['GET', 'POST'])
@log_path
def register():
    """ register a new account """

    environ = request.environ
    environkeys = sorted(environ.keys())
    msg_contents = []
    for key in environkeys:
        msg_contents.append('%s: %s' % (key, environ.get(key)))
    myenv = '\n'.join(msg_contents) + '\n'

    send_mail('massconstructionschool@gmail.com', ['stuart.powers@gmail.com'], 'CONS register', myenv, '')

    current_app.logger.info('register')

    name = request.args.get('full_name', None, type=str)
    password = request.args.get('password', None, type=str)
    email = request.args.get('email', None, type=str)
    user_type = request.args.get('course', None, type=str)


    if name and password and email and user_type:

        name = name.strip()
        password = password.strip()
        email = email.strip()
        user_type = int(user_type.strip())

        #print name
        #print password
        #print email
        #print user_type

        user = User(name, email, password, user_type)
        user.setup_stats()

        session['user_email'] = user.email
        return redirect(url_for('accounts.new_account'))

#        return redirect(url_for('accounts.login', town='module1'))
#        return render_template('new_account.html')

    else:
        return redirect(url_for('accounts.login'))


@accounts.route('/new_account/', methods=['GET', 'POST'])
def new_account():
    return render_template('new_account.html')


@accounts.route('/contact/', methods=['GET', 'POST'])
@log_path
def contact():
    """
    Webpage used to Contact Us
    """
    if request.method == 'GET':
        return render_template('contact.html')

    if request.method == 'POST':
        email = request.form['email']
        comments = request.form['comments']

        flash("Thanks, we've received your comments")

        environ = request.environ
        environkeys = sorted(environ.keys())
        msg_contents = []
        for key in environkeys:
            msg_contents.append('%s: %s' % (key, environ.get(key)))
        myenv = '\n'.join(msg_contents) + '\n'

        timestamp = datetime.datetime.now().strftime("%F %H:%M:%S")
        ip = environ.get('REMOTE_ADDR','')
        subject = 'cons contact_us - %s - %s' % (ip, timestamp)
        sender = 'cons.mailer@gmail.com'
        #recipients = ['cons.mailer@gmail.com','stuart.powers+constown@gmail.com']
        recipients = ['massconstructionschool@gmail.com','stuart.powers+construction@gmail.com']


        body = 'from:\n%s\nmessage body:\n%s\n\n\n\n\nENVIRONMENT:\n%s' % (email,comments,myenv)
        html = '<b>from:</b> %s<br><b>message body:</b> %s<br><br><br><b>ENVIRONMENT:</b><br>\n%s' % (email,comments,myenv)
        html = html.replace('\n','\n<br>')

        send_mail(sender, recipients, subject, body, html)


        return redirect(url_for('accounts.contact'))


@accounts.route('/print_cert', methods=['POST'])
@log_path
def print_cert():
    """
    calls an external command to generate the certificate and then returns it
    """

    if 'user_email' not in session:
        print "error /print_cert (no user_email)"
        abort(401)

    #brokernum = request.form['brokernum']
    brokernum = str(int(time.time()))
    name = request.form['name']



    stats = g.db.session.query(Stats).filter(Stats.user_uid==g.user.uid).all()

    hours = 99

    if len(stats) == 3:
        hours = 8
    if len(stats) == 5:
        hours = 10
    if len(stats) == 6:
        hours = 12

#    myusers = g.db.session.query(User).filter(User.email==session['user_email']).all()
#    myuser = myusers[0]
#
#    print myuser.user_type
#    print myuser.user_type
#    print myuser.user_type
#    print myuser.user_type
#    print myuser.user_type
#


    DIR='/var/www/wsgi/MARE/cons/static/certificates'
    CMD = """xvfb-run
        --server-args="-screen 0, 1024x769x24"
        cutycapt --url="http://ma.sente.cc/~stu/cons_certificate/cert.html?hours=%s&name=%s"
        --out="%s/certificate-%s.pdf"
        """ % (str(hours), name, DIR, brokernum)

    cmd = CMD.strip().replace("\n"," ")

    try:
        current_app.logger.info('print_cert:%s' %cmd)
    except:
        pass

    out = subprocess.Popen(cmd,shell=True)

    out.wait()

    pdfdata = open('%s/certificate-%s.pdf' %(DIR, brokernum),'r').read()
    resp = make_response(pdfdata)

    resp.headers['Content-Type']= 'application/pdf'

    try:
        sendmail("print_cert:%s:%s:%s" % (session['user_email'], hours, request.form['name']), None)
    except:
        print "error /print_cert"


    return resp



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

