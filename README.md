# Black Hole
Collect arbitrary HTTP requests to see what your HTTP client is sending, e.g. when debugging webhooks.

## Setup
### Install the Requirements

Create a virtualenv:
```
virtualenv venv_dir
```

Activate the virtualenv:
```
source venv_dir/bin/activate
```

Install the requirements:
```
pip install -r requirements.txt
```

### Run the Django app

Create a local settings file ``local_settings.py`` based on the example ``local_settings.example.py`` and configure the parameters according to your setup (do not share this file!):
```
cp blackhole/local_settings.example.py blackhole/local_settings.py
```

Prepare the database:
```
python manage.py migrate
```

Run the test server to verify the installation:
```
python manage.py runserver 127.0.0.1:8001
```

### Deploy the app
There are several good guides on how to deploy a Django application. Personally, I like the one from [Michal Karzynski](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/) or [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04).


## Acknowledgements
* [Django Project](https://www.djangoproject.com/)
* [django-picklefield](https://pypi.org/project/django-picklefield/)
