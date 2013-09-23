from django.db import models
from django.core.mail import send_mail
import uuid
import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


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
    user_name = models.CharField(
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
    can_invite = models.BooleanField()
    is_super_user = models.BooleanField()

    class Meta:
        ordering = ["date_invited"]

    def __unicode__(self):
        return "%s, %s: %s" % (self.last_name, self.first_name, self.date_invited)

    def send(self):
            """
            Send an invitation email to ``email``.
            """

            subject = 'invite'
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
