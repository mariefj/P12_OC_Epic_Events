# Epic_Events #

1.  [Description](#description)
2.  [Use](#use)
    1.  [setup](#setup)
    2.  [database](#database)
    3.  [admin](#admin)

## 1. Description <a name="description"></a> ##

This app has been realized as part of a project of the course
'Application developer - Python' of OpenClassrooms.


The app is a CRM helping to manage clients, events and contracts for different teams : sales, support, management.

This app is built with Django REST. Database : PostgreSQL

## 2. Use <a name="use"></a> ##

#### SETUP : <a name="setup"></a> ####

First, start by cloning the repository:

```
git clone git@github.com:mariefj/P12_OC_Epic_Events.git
```

- Access the project folder
```
cd P12_OC_Epic_Events
```

- Create a virtual environment
```
python -m venv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

- Start
```
python manage.py runserver
```

- Open in browser the following address
```
http:/127.0.0.1:8000
```

#### DATABASE : <a name="database"></a> ####

- Create database with PostgreSQL

- In Epic_Events/settings.py, change the following lines according to your settings, PASSWORD is set in Epic_Events/config.py but you can put it here or wherever you want:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'epic_events', 
        'USER': 'marie', 
        'PASSWORD': config.PASSWORD,
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}
```

- Then
```
python manage.py makemigrations
```
```
python manage.py migrate
```

#### ADMIN : <a name="admin"></a> ####

- Add a superuser

```
python manage.py createsuperuser
```

- Connect to http://127.0.0.1:8000/admin/ and create a manager profile to be able to access to Django admin site and add clients, contracts or events.