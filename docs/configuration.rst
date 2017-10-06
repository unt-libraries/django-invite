#############
Configuration
#############

Invite provides 4 configurable settings that can be customized by including them in your
projects settings files.

Settings
--------

``INVITE_LOGOUT_REDIRECT_URL``
..............................

**Optional**

**Default** : ``reverse('invite:index')``

Where your users would be redirected to upon logging out from within the Invite app.


``INVITE_SIGNUP_SUCCESS_URL``
.............................

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


``INVITE_SHOW_EMAILS``
......................

**Optional**

**Default** : ``False``

Whether or not to show superusers and users with invitation permission the emails associated with invitations/registrations on the accounts page.


``INVITE_OPEN_INVITE_CUTOFF``
.............................

**Optional**

**Default** : ``None``

Defines a time period (in days back from today) for displaying open invitations. Open invitations older than that will not be shown on the accounts page.
A value of None will be interpreted to mean that all open invitations should be shown, while a value of 0 means none should be shown.


``INVITE_REGISTRATION_CUTOFF``
..............................

**Optional**

**Default** : ``None``

Defines a time period (in days back from today) for displaying registrations. Registrations older than that will not be shown on the accounts page.
A value of None will be interpreted to mean that all registrations should be shown, while a value of 0 means none should be shown.

