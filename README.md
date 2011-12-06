MARE
----------


**This is a rebuild of Shawn's very broken MARE site.**

how to get started
------------------

1. ```cd ~```

2. ```virtualenv --python=python2.7 --no-site-packages mare_env```

3. ```cd mare_env && git clone git@github.com:sente/mare.git```

4. ```source bin/activate```

5. ```cd mare```

5. ```pip install -r requirements.txt```

6. ```export MAREPASS=<passwd>```

7. ```python manage.py create_db```

8. ```python manage.py full_test```

9. ```python manage.py runserver```

