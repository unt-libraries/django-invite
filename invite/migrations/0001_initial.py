# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_code', models.CharField(default=uuid.uuid4, help_text=b'unique id, generated on email submission', unique=True, max_length=36, editable=False)),
                ('first_name', models.CharField(max_length=36)),
                ('last_name', models.CharField(max_length=36)),
                ('username', models.CharField(max_length=36)),
                ('email', models.EmailField(help_text=b"the potential member's email address", max_length=41)),
                ('custom_msg', models.TextField(blank=True)),
                ('date_invited', models.DateField(help_text=b'the day on which the superuser invited the potential member', auto_now=True)),
                ('is_super_user', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['date_invited'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InviteItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('username', models.CharField(max_length=150)),
                ('greeting', models.TextField(blank=True)),
                ('is_super_user', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True)),
                ('permissions', models.ManyToManyField(to='auth.Permission', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordResetInvitation',
            fields=[
                ('invitation_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='invite.Invitation')),
            ],
            options={
            },
            bases=('invite.invitation',),
        ),
        migrations.AddField(
            model_name='invitation',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='permissions',
            field=models.ManyToManyField(to='auth.Permission'),
            preserve_default=True,
        ),
    ]
