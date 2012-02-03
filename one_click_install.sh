#!/bin/sh

# one click install of http://github.com/sente/mare/
# this file should be SOURCED
# `source one_click_install.sh`


test -x /usr/bin/python2.6 && PYTHON_VERSION=python2.6
test -x /usr/bin/python2.7 && PYTHON_VERSION=python2.7

virtualenv --python=${PYTHON_VERSION} --no-site-packages mare_env

cd mare_env

git clone git@github.com:sente/mare.git

source bin/activate

cd mare

pip install --log=piplog.log -r requirements.txt

sqlite3 mare/dev.db < mare/data/schema.sql
sqlite3 mare/dev.db < mare/data/load_data.sql

echo "setup complete, run: python manager.py runserver -t 0.0.0.0 -p 5500"
# python manager.py runserver -t 0.0.0.0 -p 5500

