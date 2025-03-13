# Django Invite  

[![Build Status](https://github.com/unt-libraries/django-invite/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/unt-libraries/django-invite/actions)

Invite is a Django app for inviting new users to your new or existing Django project.

## Dependencies

* Python 3.8 - 3.11
* Django 4.2.x

## Documentation

Documentation, including installation instructions, can be viewed online at:

[http://django-invite.readthedocs.org](http://django-invite.readthedocs.org)

## Development

```sh
$ git clone https://github.com/unt-libraries/django-invite

$ cd django-invite
```

Install the app and test requirements.
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
$ pytest
```

Run the tests against all supported versions of Django, and run a flake8 check.
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
- [Trey Clark](http://github.com/clarktr1)