MARE
----------

**This is a rebuild of Shawn's very broken MARE site.**

How to get started
------------------

```bash

myenv=mare_env

test -x /usr/bin/python2.6 && PYTHON_VERSION=python2.6
test -x /usr/bin/python2.7 && PYTHON_VERSION=python2.7

virtualenv --python=${PYTHON_VERSION} --no-site-packages $myenv

cd $myenv && git clone git@github.com:sente/mare.git
source bin/activate
cd mare


pip install --log=piplog.txt -r requirements.txt
pip freeze > pip_freeze.txt

sqlite3 mare/dev.db < mare/data/schema.sql
sqlite3 mare/dev.db < mare/data/load_data.sql

python manager.py runserver -t 0.0.0.0 -p 5500
```

After running the above code point your browser to 127.0.0.1:5500 and login as stuart.powers@gmail.com:test


For the extremely lazy
----------------------

download [one_click_install.sh](one_click_install.sh)

```bash
source one_click_install.sh
```

