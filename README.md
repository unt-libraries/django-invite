# Django Invite  

[![Build Status](https://travis-ci.org/unt-libraries/django-invite.svg?branch=master)](https://travis-ci.org/unt-libraries/django-invite)

Invite is a Django app for inviting new users to your new or existing Django project.

## Dependencies

* Python 3.7.x
* Django 2.2.x

## Documentation

Documentation, including installation instructions, can be viewed online at:

[http://django-invite.readthedocs.org](http://django-invite.readthedocs.org)

## Development

```sh
$ git clone https://github.com/unt-libraries/django-invite

$ cd django-invite
```

Install the requirements.
```sh
$ pip install -r requirements.txt
```

Run the migrations.
```sh
$ ./manage.py migrate
```

Create a superuser.
```sh
$ ./manage.py createsuperuser
```

Run the development server.
```sh
$ ./manage.py runserver
```

Run the tests.
```sh
$ ./manage.py test
```

Run the tests against all supported versions of Django.
```sh
$ pip install tox

$ tox
```

## License

See LICENSE.

## Acknowlegments

Invite was developed at the UNT Libraries.

Contributors:

- [Joey Liechty](http://github.com/yeahdef)
- [Damon Kelley](http://github.com/damonkelley)
- [Mark Phillips](http://github.com/vphill)
- [Lauren Ko](http://github.com/ldko)
- [Gio Gottardi](http://github.com/somexpert)
- [Madhulika Bayyavarapu](http://github.com/madhulika95b)
