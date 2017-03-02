#############
Configuration
#############

Invite provides 4 configurable settings that can be customized by including them in your
projects settings files.

Settings
--------

``INVITE_LOGOUT_REDIRECT_URL``
...............................

**Optional**

**Default** : ``reverse('invite:index')``

Where your users would be redirected to upon logging out from within the Invite app.


``INVITE_SIGNUP_SUCCESS_URL``
...............................

**Optional**

**Default** : ``reverse('invite:index')``

Where the user will be redirected to upon successfully completing the signup form.

``INVITE_SERVICE_NAME``
.......................

**Optional**

**Default** : ``Site.objects.get_current().domain``

This setting is used in the to create a customized email that is sent to the invited user. 


``INVITE_DEFAULT_FROM_EMAIL``
.............................

**Optional**

**Default** : ``django.conf.settings.DEFAULT_FROM_EMAIL``

The 'From' field for emails sent via the Invite app.

