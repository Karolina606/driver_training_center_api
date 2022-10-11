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