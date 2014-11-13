###########
Permissions
###########

Like standard Django models, there are a number of permissions associated with the invite models. One in particular is important, as it determines
which users are allowed to invite new users your project.

``invite.add_invitation``

.. note::
    If a user does not have this permission, they will still have limited access to pages included in the Invite app. Such users will only be shown a list of active accounts. They will not have access to the open invitations or the invitation form.
