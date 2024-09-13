Change Log
==========

5.0.0
-----
* Upgraded Django support from 2.2 to 4.2.
* Dropped support for Python 3.7.
* Set same redirect URL for password resets as for setting an initial password.

4.1.0
-----
* Added support for Python 3.8 - 3.11.
* Dropped Travis CI integration.
* Moved CI to Github Actions.
* Switched to using pytest to run test suite.

4.0.0
-----

* Added Django 2.2 support.
* Dropped support for Django 1.11.

3.0.0
-----

* Added Python 3.7 support.
* Removed Python 2.7 support.
* Added application 'invite' application namespace.
* Fixed bug that caused invite form's submit button to be disabled when a maintenance message was active.

2.1.0
-----

* Added filtering to the groups and permissions selection boxes on the invitation page.
* Added check for the usernames and emails on the invitation page to show whether they're in use before submitting the form.
* Added setting to show emails on the accounts page to superusers and users who can create invitations.
* Added setting to limit the timeframe for showing open invitations and registrations on the accounts page.
* Tweaked the UI on the invitations and accounts pages.
  * Resized and moved some of the inputs.
  * Improved responsiveness.
  * Improved behavior and location of the "add" button on the invitation form.
  * Made sure username is displayed correctly.
  * Stopped duplicate error messages from being shown.
  * Made sure errors get removed when their form row is removed.
  * Updated wording and information organization on the accounts page.
* Fixed remaining sorting difference that occurred after resending invitation email.
* Changed the dev environment to output emails directly to stdout.

2.0.2
-----

* Fixed bug that prevented password resets when no SITE_ID was set.
* Corrected usage of deprecated setting.
* Fixed sorting difference that occurred after resending invitation email.

2.0.1
-----

* Fixed bug that prevented signing up for an account when no SITE_ID was set.

2.0.0
-----

* Updated to work with Django 1.8.
* Removed requirement for the SITE_ID setting to be used. SITE_ID can still be used, but now, if it isn't, the site will be determined based on a domain match of your defined sites.

1.0.2
-----

* Last version with support for Django 1.5 - 1.7
