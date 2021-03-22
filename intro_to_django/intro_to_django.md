# Introduction to Django

## What is Django

- Python web framework, focused on providing 'boiler plate' code for rapid development
- Useful for easily developing database centered websites
- Uses the model - view - controller (MVC) arhcitecture
    - model : object-relational mapper (ORM) for interacting between data models and relational databases, manages data for the application
    - view : web templating system for processing HTTP requests (core logic), can have multiple views for same model data
    - controller : URL dispatcher, converts commands / user input and passes this to models or views

- Other alternatives:
    - Flask (Python)
    - Ruby on Rails
    - Laravel
    - Spring
    - many, many others


## How do you Django

- install with `pip install django`
- start new project with `django-admin startproject my_site`
- produces basic framework:

```
- my_site/
    - manage.py
    - my_site/
        - __init__.py
        - settings.py
        - urls.py
        - wsgi.py
```

- `manage.py` : Django python script for managing project (i.e. running the webserver)
- `__init__.py`: defines dir as Python package
- `settings.py`: contains all website settings
- `urls.py`: defines URLs - view mapping (i.e. what page URLs run what code)
- `wsgi.py`: Web Server Gateway Interface, Django boilerplate code for running as web server

<br></br>

- Django development is centred around creating 'apps' that define each part of the site.
- create a new app with from Django project dir `python3 manage.py startapp my_site_app`
- creates a new app inside the Django dir with the following files

```
- my_site/
    - manage.py
    - my_site/
        - __init__.py
        - settings.py
        - urls.py
        - wsgi.py
    - my_site_app/
        - admin.py
        - apps.py
        - models.py
        - tests.py
        - views.py
        - __init__.py
        migrations/
```

- `admin.py`: used to define admin models for changing admin interface
- `apps.py`: can help with definig app config / attributes
- `models.py`: defines database tables and relations
- `tests.py`: empty file to define unit tests
- `views.py`: core functions and logic, processes data between user and database


## Core Django concepts

### Models

- each class in `models.py` defines a table in database
- after each change in models you have to migrate changes to the db
    - `python manage.py makemigrations`
    - `python manage.py migrate`
- lots of different types - TextField, CharField, DateField, BooleanField etc.
- can add validation to database fields to sanitise data
- link tables together with `models.ForeignKey`
- example `models.py`:

https://github.com/eastgenomics/panel_palace/blob/main/panel_database/models.py

```
class Panel(models.Model):
    panelapp_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    panel_type = models.ForeignKey("PanelType", on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "panel"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["panelapp_id"])
        ]
```

### Views

- script to store all functions to manage logic
- handle user input / what is passed to templates
- can use to return data from database and pass to user etc.
- example `views.py`:

```
def find_some_data(request):
    """View to return data for a request from database"""
    data = model.thing.objects.all()

    data_dict = {}
    data_dict['data'] = data

    return render(request, 'some_url/my_template.html', data_dict)
```

### URLs

- maps URL patterns to views
- https://docs.djangoproject.com/en/3.1/topics/http/urls/
- example in `urls.py`:
```
urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<int:year>/', views.year_archive),
    path('articles/<int:year>/<int:month>/', views.month_archive),
    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
```


### Templates

- each page should have a template, written in HTML
- pass data from view to template
- https://docs.djangoproject.com/en/3.1/topics/templates/
- good practice to store an apps templates inside a template dir in the app:
```
- my_site/
    - manage.py
    - my_site/
    - my_site_app/
        - admin.py
        - apps.py
        - models.py
        - tests.py
        - views.py
        - __init__.py
        - templates/
            - my_site_app/
                - my_template.html
        migrations/
```
- example template:

```
<html>
  <head>
    <title>Band Listing</title>
  </head>
  <body>
    <h1>All Bands</h1>
    <ul>
    {% for band in bands %}
      <li>
        <h2><a href="{{ band.get_absolute_url }}">{{ band.name }}</a></h2>
        {% if band.can_rock %}<p>This band can rock!</p>{% endif %}
      </li>
    {% endfor %}
    </ul>
  </body>
</html>
```

- make things pretty with the wonders of bootstrap and css


### Forms

- used to define fields on a template that a user passes data with
- allows for validating data at user side
- https://docs.djangoproject.com/en/3.1/topics/forms/
- example `forms.py`:

```
from django import forms

class BandContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.TextField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

```

### Static Files

- files such as images and css should be stored in a static dir
- keeps organised & allows for importing static files

```
- my_site/
    - manage.py
    - my_site/
        - __init__.py
        - settings.py
        - urls.py
        - wsgi.py
    - static/
        - images/
        - js/
        - css/
```

### settings.py

- `settings.py` file used to store all site settings
- used to register new apps, define database connections, logging etc.
- good practice to store auth keys and passwords etc in a separate config file and import, do not push passwords into GitHub
- example: https://github.com/eastgenomics/Genetics_Ark/blob/ark_v2/ga_core/settings.py


### Other random things

- css / js:
    - can provide css and js (JavaScript) to template either via a CDN link (content delivery network) or store files in `/static/`
    - CDN: `<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
    - local: <script type="text/javascript" src="/static/js/jquery.min.js"></script>
- good practice to have a `base.html` template file that all others extend from
    - load base template with `{% extends 'base.html' %}`
    - https://github.com/eastgenomics/Genetics_Ark/tree/ark_v2/genetics_ark/templates


## Resources

- example Django site:
    - Genetics Ark: https://github.com/eastgenomics/Genetics_Ark/tree/ark_v2

- docs:
    - https://www.djangoproject.com/start/
    - Basic HTML & CSS: https://www.w3schools.com/html/ & https://www.w3schools.com/css/

- guides / tutorials
    - https://docs.djangoproject.com/en/3.1/intro/tutorial01/
    - https://tutorial.djangogirls.org/en/
    - https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
