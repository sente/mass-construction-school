# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, flash, request, render_template, session, g, abort, current_app, make_response
from werkzeug import generate_password_hash, check_password_hash
import time


import logging
import subprocess

from mare.models import Stats, User, Video

#from mare.extensions import db
from mare.extensions import mail
from mare.extensions import Message
from mare.extensions import SQLAlchemy
from mare.extensions import sendmail

accounts = Blueprint('accounts', __name__)


#def sendmail(body,html):
#    msg = Message("MARE CONTACT US",
#                  sender="stu@sente.cc",
#                  recipients=["stuart.powers@gmail.com"])
#    msg.body = body
#    msg.html = html
#
#    mail.send(msg)




@accounts.before_request
def before_request():
    """Make sure we are connected to the database each request and look
    up the current user so that we know he's there.
    """
    g.user = None
    g.db = SQLAlchemy()
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
        if s.watched == s.video.duration:
            completed.append(s.video)
        else:
            incompleted.append(s.video)
    if len(incompleted) == 0:
#        try:
#            out = subprocess.Popen('/var/www/wsgi/MARE/mare/scripts/generate_certificate.py')
#            out.wait()
            finished = True
##            flash('created PDF')
#        except:
#            flash("ERROR")
#    finished = True
    return render_template('videos.html' , videos=videos, completed=completed, incompleted=incompleted, finished=finished, stats=stats)


@accounts.route('/video/', methods=['GET', 'POST'])
def video():
    if 'user_email' not in session:
        print "error"
        abort(401)

    user_id = g.user.uid
    video_id  = request.args.get('video_id', 1, type=int)
    dev = request.args.get('dev', 0, type=int)


    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]

    if dev != 0:
        flash('in debug mode')

    video = g.db.session.query(Video).filter(Video.id == video_id).first()
    return render_template('video.html', email=g.user.email, video=video, user=g.user, stat=mystat, dev=dev)


@accounts.route('/watch/', methods=['GET', 'POST'])
def watch():
    if 'user_email' not in session:
        print "error"
        abort(401)
    user_id = request.args.get('user_id', None, type=int)
    video_id = request.args.get('video_id', None, type=int)
    timestamp = int(request.args.get('time', 0, type=float))


    mystats = g.db.session.query(Stats).filter(Stats.video_id==video_id).filter(Stats.user_uid==user_id).all()
    mystat = mystats[0]

    if mystat.status != mystat.video_id:
        return "sadness"

    if mystat.watched < timestamp:
        mystat.watched = timestamp
        g.db.session.commit()

    return '%d watch' % mystats[0].watched


@accounts.route('/finish/', methods=['GET', 'POST'])
def finish():
    if 'user_email' not in session:
        print "error"
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
        print "error"
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
        sendmail('%s:%s' %(email,comments),comments)
        return redirect(url_for('accounts.contact'))


@accounts.route('/print_cert', methods=['POST'])
def print_cert():


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

#    out = subprocess.Popen('/var/www/wsgi/MARE/mare/scripts/generate_certificate.py "%s" "%s"' %(name, brokernum), shell=True)
    out.wait()

    pdfdata = open('%s/certificate-%s.pdf' %(DIR,brokernum),'r').read()
    resp = make_response(pdfdata)

    resp.headers['Content-Type']= 'application/pdf'
#    response.headers['Content-Type']: application/pdf

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
        print "error"
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
                return "your password has been emailed"
            else:
                return "ERROR"
        else:
            return "ERROR bad form types"

        return "ERRROR"




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

