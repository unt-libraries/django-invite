Change Log
==========

2.0.2
-----

* Fixed bug that prevented password resets when no SITE_ID was set.
* Corrected usage of deprecated setting.
* Fixed sorting difference that occured after resending invitation email.

2.0.1
-----

* Fixed bug that prevented signing up for an accoung when no SITE_ID was set.

2.0.0
-----

* Updated to work with Django 1.8.
* Removed requirement for the SITE_ID setting to be used. SITE_ID can still be used, but now, if it isn't, the site will be determined based on a domain match of your defined sites.

1.0.2
-----

* Last version with support for Django 1.5 - 1.7
