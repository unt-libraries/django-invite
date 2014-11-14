##########
Quickstart
##########

Requirements
------------
* The Django Sites framework must be installed. See the `Django Docs <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ for more information.

.. note::
    If the Sites framework was not previously install, make sure you configure the domain and name. Those values are used to create urls for invited users. Upon installation of the Sites framework, both values default to `example.com` 
Installation
------------

* ``pip install git+https://github.com/unt-libraries/django-invite.git@v1.0.0``

* Add ``invite`` to your ``INSTALLED_APPS``
* Run ``./manage.py syncdb``
* Add the following to your root ``urls.py``. ::

    urlpatterns = [
        ...
        url(r'^invite/', include('invite.urls', namespace='invite'))
    ]


How it Works
------------

Invitations are sent via email with a activation link for each invited user. When the new user follows the link, they are given a form to edit their information and provide a password. Once successfully submitted, the activation link for that user is no longer valid.

After the a new user completes the signup form, he/she is automatically authenticated and redirected to the value of ``settings.INVITE_SIGNUP_SUCCESS_URL``

Authentication is required by most views in the Invite app, and only users with the correct permission are able to invite new users (see :doc:`permissions`)
