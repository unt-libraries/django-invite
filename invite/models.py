from django.contrib.auth.models import Permission, Group
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
import uuid

from . import settings as app_settings


class InviteItem(models.Model):
    """This is the model used to generate the forms."""

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    username = models.CharField(max_length=150)
    greeting = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    is_super_user = models.BooleanField(default=False)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class AbstractInvitation(models.Model):
    """Defines an abstract model with basic invitation fields."""

    activation_code = models.CharField(
        max_length=36,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="unique id, generated on email submission",
    )

    first_name = models.CharField(
        max_length=36,
    )

    last_name = models.CharField(
        max_length=36,
    )

    username = models.CharField(max_length=36)

    email = models.EmailField(
        max_length=41,
        help_text="the potential member's email address",
    )

    custom_msg = models.TextField(blank=True)

    date_invited = models.DateField(
        auto_now=True,
        help_text="the day on which the superuser invited the potential member",
    )

    permissions = models.ManyToManyField(Permission)
    groups = models.ManyToManyField(Group)
    is_super_user = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s, %s: %s" % (
            self.last_name,
            self.first_name,
            self.date_invited)

    class Meta:
        abstract = True
        ordering = ["date_invited"]


class Invitation(AbstractInvitation):
    """Defines a model for new user invitations."""

    def send(self, request=None):
        """Sends an invitation email to ``self.email``."""

        subject = 'You have been invited to join the %s' % (
            app_settings.get_service_name(request=request))
        message = render_to_string(
            'invite/invitation_email.txt',
            {
                'domain': Site.objects.get_current(request=request).domain,
                'service_name': app_settings.get_service_name(request=request),
                'activation_code': self.activation_code,
                'custom_msg': self.custom_msg,
                'permissions': self.permissions.all()
            }
        )

        send_mail(subject, message, app_settings.INVITE_DEFAULT_FROM_EMAIL, [self.email])


class PasswordResetInvitation(AbstractInvitation):
    """Defines a model for invitations created for password resets."""

    def send(self, request=None):
        """Sends an invitation email to ``self.email``."""

        subject = 'Password Reset: %s' % (app_settings.get_service_name(request=request))
        message = render_to_string(
            'invite/reset_email.txt',
            {
                'first_name': self.first_name,
                'username': self.username,
                'domain': Site.objects.get_current().domain,
                'reset_code': self.activation_code,
            }
        )

        send_mail(subject, message, app_settings.INVITE_DEFAULT_FROM_EMAIL, [self.email])

    def send_confirm(self, request=None):
        """Sends an confirmation email to ``self.email``."""

        subject = 'Password Changed: %s' % (app_settings.get_service_name(request=request))
        message = render_to_string(
            'invite/reset_confirm_email.txt',
            {
                'first_name': self.first_name,
                'username': self.username,
                'domain': Site.objects.get_current().domain,
                'reset_code': self.activation_code,
            }
        )

        send_mail(subject, message, app_settings.INVITE_DEFAULT_FROM_EMAIL, [self.email])
