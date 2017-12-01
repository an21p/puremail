# Define the project components
[Tutorial](https://docs.docker.com/compose/django/#define-the-project-components)

```
 docker-compose run web django-admin.py startproject puremail .
 docker-compose up
 ```


# Connect the database
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
```
# Migrations
- Plug the appConfig in the INSTALLED_APPS
- Change your models (in `models.py`).
- Run `python manage.py makemigrations` to create migrations for those changes
- Run `python manage.py migrate` to apply those changes to the database.

#### Apply Migrations
```
docker-compose down
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up
```

#### See the sql
```
 docker-compose run web python manage.py sqlmigrate polls 0001
```

# Fixtures
#### Export
```
docker-compose run web python manage.py dumpdata --format=json --indent=4 -o students/fixtures/001.json
```
#### import
```
docker-compose run web python manage.py loaddata students/fixtures/001.json
```

# Create admin user
```
docker-compose stop
docker-compose run web python manage.py createsuperuser
docker-compose start
```

# Email Setup

[Sending Email Doc](https://docs.djangoproject.com/en/1.11/topics/email/#topic-email-console-backend)

[Gmail Example](https://gilang.chandrasa.com/blog/sending-email-in-django-with-gmail/)

#### Current Email Setup (only for development)
run this on local machine
```
python3 -m smtpd -n -c DebuggingServer localhost:1025
```


# [Emails](https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html)
```
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@ubreal.co.uk', ['pishias92@gmail.com'], fail_silently=False)
```

## Settings for email
```
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'xxxxxxxx'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'
EMAIL_MAIN = 'noreply@xxxxxxxx.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
or
```
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = "xxx"
#os.environ["SENDGRID_API_KEY"]
```

# Security

## File Encryption
1. encrypt ID uploads before saving/decrypt when viewing (only if owner or admin) [Library 1](https://github.com/danielquinn/django-encrypted-filefield)
[Library 2](https://github.com/ruddra/django-encrypt-file)


## File Storage
[AWS](https://www.codingforentrepreneurs.com/blog/s3-static-media-files-for-django/)


# Going Live
[NGINX-django setup](http://ruddra.com/2016/08/14/docker-django-nginx-postgres/)
