What to do, to make app work:
* Install Python, here Python3.8
* Install Django: `python -m pip install django`
* Install PostgreSQL, here PostgreSQL14
* PostgreSQL install connector: `pip install psycopg2`, ` python -m pip install psycopg2`
* Install Django REST Framework: `pip install djangorestframework`, `python -m pip install djangorestframework`

What to do, to generate UML diagram:
* Install python extensions: `pip install django-extensions`, `python -m pip install django-extensions`
* Add `django-extensions` to installed apps:
  ``` 
    INSTALLED_APPS = (
      ...
      'django_extensions',
      ...
    ) 
  ```
* Install pydotplus and graphviz: `pip install pydotplus`, `python -m pip install pydotplus`,
* Install graphviz: `pip install pygraphviz`, `python -m pip install pygraphviz` or for Windows: [pygraphviz](https://pygraphviz.github.io/documentation/stable/install.html])
* Make diagram: `python manage.py graph_models -a -o myapp_models.png`

What to do, to use swagger:
* Install swagger for python: `pip install django-rest-swagger`, `python -m pip install django-rest-swagger`


What to do, to setup groups, permissions and driving licesne categories:
* Run django management scripts: `python manage.py init_groups` and `python manage.py init_driving_license_categories`


What to do, to add authorization by token: 
* Install `pip install djangorestframework django-cors-headers==3.11.0 djangorestframework-simplejwt==5.0.0 PyJWT==2.3.0`, 
  `python -m pip install djangorestframework django-cors-headers==3.11.0 djangorestframework-simplejwt==5.0.0 PyJWT==2.3.0`

What to do, to add encryption:
* Install `pip install django_cryptography`, `python -m pip install django_cryptography`

What to do, to add encryption:
* Install `pip install django-pgcrypto`, `python -m pip install django-pgcrypto`
* Install `pip3 install pycryptodome`, `python -m pip3 install pycryptodome`