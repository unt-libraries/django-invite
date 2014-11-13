##########
Quickstart
##########

Requirements
------------
* The Django Sites framework must be installed. See the `Django Docs <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ for more information.

Installation
------------

* ``pip install git+git://github.com/unt-libraries/django-invite.git@v1``

* Add ``invite`` to your ``INSTALLED_APPS``
* Run ``./manage.py syncdb``
* Add the following to your root ``urls.py``. ::

    urlpatterns = [
        ...
        url(r'^invite/', include('invite.urls', namespace='invite'))
    ]

