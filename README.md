MARE
----------


**This is a rebuild of Shawn's very broken MARE site.**

How to get started
------------------


```

cd $HOME

virtualenv --python=python2.7 --no-site-packages mare_env  

#virtualenv --python=python2.6 --no-site-packages mare_env  # no 2.7? try 2.6...
#virtualenv --python=python --no-site-packages mare_env # meh...

cd mare_env && git clone git@github.com:sente/mare.git

source bin/activate

cd mare

pip install -r requirements.txt

export MAREPASS=YOUREMAILPASSWORD #change this to the password

python manage.py create_db

python manage.py full_test

python manage.py runserver -t 0.0.0.0 -p 5500

```


