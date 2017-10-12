# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0002_abstract_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='date_invited',
            field=models.DateField(help_text=b'the day on which the superuser invited the potential member', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='passwordresetinvitation',
            name='date_invited',
            field=models.DateField(help_text=b'the day on which the superuser invited the potential member', auto_now_add=True),
        ),
    ]
