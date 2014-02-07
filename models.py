from django.contrib.auth.models import User, Permission, Group
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.files import File
from django.db import models
import settings
import uuid
from cStringIO import StringIO


class InviteItem(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    username = models.CharField(max_length=150)
    greeting = models.CharField(max_length=150, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    is_super_user = models.BooleanField()

    def __unicode__(self):
        return self.name + " (" + str(self.list) + ")"


class Invitation(models.Model):

    def make_uuid():
        return str(uuid.uuid4())

    activation_code = models.CharField(
        max_length=36,
        default=make_uuid,
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
    username = models.CharField(
        max_length=36,
    )
    email = models.EmailField(
        max_length=41,
        help_text="the potential member's email address",
    )
    custom_msg = models.CharField(
        max_length=256,
    )
    date_invited = models.DateField(
        auto_now=True,
        help_text="the day on which the superuser invited the potential member",
    )
    permissions = models.ManyToManyField(Permission)
    groups = models.ManyToManyField(Group)
    is_super_user = models.BooleanField()

    class Meta:
        ordering = ["date_invited"]

    def __unicode__(self):
        return "%s, %s: %s" % (self.last_name, self.first_name, self.date_invited)

    def send(self):
            """
            Send an invitation email to ``email``.
            """

            subject = 'You have been invited to join %s' % (settings.SERVICE_NAME)
            message = render_to_string(
                'invite/invitation_email.txt',
                {
                    'domain': Site.objects.get_current().domain,
                    'service_name': settings.SERVICE_NAME,
                    'activation_code': self.activation_code,
                    'custom_msg': self.custom_msg,
                }
            )

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email])
