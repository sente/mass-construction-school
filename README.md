MARE
----------

**This is a rebuild of Shawn's very broken MARE site.**

How to get started
------------------


```bash
cd $HOME

virtualenv --python=python2.7 --no-site-packages mare_env

cd mare_env && git clone git@github.com:sente/mare.git

source bin/activate

cd mare

pip install -r requirements.txt

sqlite3 mare/dev.db < mare/data/schema.sql
sqlite3 mare/dev.db < mare/data/load_data.sql

python manager.py runserver -t 0.0.0.0 -p 5500

```

