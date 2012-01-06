#!/usr/bin/python

import subprocess

import sys


#out = subprocess.Popen('xvfb-run --server-args="-screen 0, 1024x769x24" cutycapt --url="http://sente.cc/stu/cert.html?brokernum=%d&name=%s" --out=certificate-%d.pdf' % (g.user.brokernum, g.user.name, g.user.brokernum),shell=True)

DIR = '/var/www/wsgi/MARE/mare/static/certificates'

brokernum = 12345
name = 'Stuart Powers'


CMD = """xvfb-run
    --server-args="-screen 0, 1024x769x24"
    cutycapt --url="http://sente.cc/stu/cert.html?brokernum=%s&name=%s"
    --out=%s/certificate-%d.pdf
    """ % (brokernum, name, DIR, brokernum)


cmd = CMD.strip().replace("\n"," ")
out = subprocess.Popen(cmd,shell=True)

