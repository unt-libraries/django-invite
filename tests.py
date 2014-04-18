from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.test.client import Client
from django.contrib.auth.models import User, Group

import unittest
from unittest import skipIf
import platform
import time
import requests
try: import simplejson as json
except ImportError: import json
import settings
import mock
from .models import Invitation, PasswordResetInvitation


class TestOperations(unittest.TestCase):

    def test_invite_creation(self):
        '''creates an invite and check to see if we can send the email'''
        i = Invitation.objects.create(
            email='joeyliechty@supergreatmail.com',
        )
        i.save()
        self.assertTrue(Invitation.objects.count() > 0)

    @mock.patch('invite.models.send_mail')
    def test_email_send(self, mock_django_mailer):
        '''
        since we trust the django mailer, and we don't want to do time wasting
        tests that do actual network activity, we'll use mock to ensure that
        the mailer is called with the correct arguments by the model
        '''
        i = Invitation.objects.create(
            email='1234testemail@noone.ghost',
            username='test',
            first_name='test',
            last_name='test',
        )
        message = render_to_string(
            'invite/invitation_email.txt',
            {
                'domain': Site.objects.get_current().domain,
                'service_name': settings.SERVICE_NAME,
                'activation_code': i.activation_code,
                'custom_msg': i.custom_msg,
            }
        )
        i.send()
        mock_django_mailer.assert_called_with(
            'You have been invited to join the %s' % (settings.SERVICE_NAME),
            message,
            settings.DEFAULT_FROM_EMAIL,
            [i.email],
        )

    def test_password_reset_invite_creation(self):
        '''creates an invite and check to see if we can send the email'''
        i = PasswordResetInvitation.objects.create(
            email='joeyliechty@supergreatmail.com',
        )
        i.save()
        self.assertTrue(Invitation.objects.count() > 0)

    @mock.patch('invite.models.send_mail')
    def test_password_reset_email_send(self, mock_django_mailer):
        '''
        since we trust the django mailer, and we don't want to do time wasting
        tests that do actual network activity, we'll use mock to ensure that
        the mailer is called with the correct arguments by the model
        '''
        i = PasswordResetInvitation.objects.create(
            email='1234testemail@noone.ghost',
            username='test',
            first_name='test',
            last_name='test',
        )
        subject = 'Password Reset: %s' % (settings.SERVICE_NAME)
        message = render_to_string(
            'invite/reset_email.txt',
            {
                'first_name': i.first_name,
                'username': i.username,
                'domain': Site.objects.get_current().domain,
                'reset_code': i.activation_code,
            }
        )
        i.send()
        mock_django_mailer.assert_called_with(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [i.email],
        )


class TestViews(unittest.TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.get_or_create(
            username='kingkong',
            email='test@test.test',
            password='test',
        ) 
        self.i = Invitation.objects.create(
            username='asdf',
            first_name='test',
            last_name='test',
            email='test@test.test'
        ) 
        self.psi = PasswordResetInvitation.objects.create(
            email='1234testemail@noone.ghost',
            username='anotherape',
            first_name='test',
            last_name='test',
        )

    def tearDown(self):
        User.objects.all().delete()
        PasswordResetInvitation.objects.all().delete()
        Invitation.objects.all().delete()

    def test_multiple_email(self):
        '''
        make sure that the multiple email invitation sends to all emails.
        '''
        my_admin = User.objects.create_superuser('test', 'myemail@test.com', 'test')
        self.c.login(username='test', password='test')
        response = self.c.post(
            '/accounts/invite/',
            {
                u'form-INITIAL_FORMS': [u'0'],
                u'form-MAX_NUM_FORMS': [u''],
                u'form-TOTAL_FORMS': [u'3'],
                u'form-1-username': [u'two'],
                u'form-1-email': [u'two@two.com'],
                u'form-1-first_name': [u'ieie'],
                u'form-1-last_name': [u'ueueu'],
                u'form-2-email': [u'thr@thr.com'],
                u'form-2-first_name': [u'oiawbeg'],
                u'form-2-username': [u'three'],
                u'form-2-last_name': [u'oaweinf'],
                u'form-0-email': [u'asdf@one.com'],
                u'form-0-username': [u'one'],
                u'form-0-last_name': [u'fdsa'],
                u'form-0-first_name': [u'asdf'],
                u'form-0-greeting': [u''],
            },
        )
        invite0 = Invitation.objects.get(email='asdf@one.com')
        invite1 = Invitation.objects.get(email='two@two.com')
        invite2 = Invitation.objects.get(email='thr@thr.com')
        # assert the distint emails are attached to separate invites
        self.assertEqual(invite0.email, 'asdf@one.com')
        self.assertEqual(invite0.username, 'one')
        self.assertEqual(invite1.email, 'two@two.com')
        self.assertEqual(invite1.username, 'two')
        self.assertEqual(invite2.email, 'thr@thr.com')
        self.assertEqual(invite2.username, 'three')

    def test_invite_correct_group_selected(self):
        '''
        since we have to do some hacky group ordering chop around stuff,
        let's make sure that the invitation retains the right group.
        '''
        prod_groups = [
            'UNT Archives',
            'Boyce',
            'Palestine',
            'texgen',
            'unt rare books',
            'archives civil war',
            'unt college of visual arts',
        ]
        for g in prod_groups:
            Group.objects.create(name=g)

        my_admin = User.objects.create_superuser('test', 'myemail@test.com', 'test')
        self.c.login(username='test', password='test')
        response = self.c.post(
            '/accounts/invite/',
            {
                u'form-MAX_NUM_FORMS': [u''],
                u'form-0-email': [u'joeyliechty@gmail.com'],
                u'form-TOTAL_FORMS': [u'1'],
                # archives civil war, boyce ditto, texas general land office
                u'form-0-groups': [u'2', u'4', u'1'],
                u'form-0-username': [u'jejfi'],
                u'form-INITIAL_FORMS': [u'0'],
                u'form-0-last_name': [u'a'],
                u'form-0-first_name': [u'a'],
                u'form-0-greeting': [u'']
            }
        )
        invite0 = Invitation.objects.get(email='joeyliechty@gmail.com')
        # assert the invitation has the correct groups
        self.assertEqual(invite0.groups.all()[0].name, 'Boyce')
        self.assertEqual(invite0.groups.all()[1].name, 'texgen')
        self.assertEqual(invite0.groups.all()[2].name, 'UNT Archives')

    def test_amnesia_email_submit(self):
        response = self.c.post('/accounts/amnesia/', {'email': 'avowin@test.test'})
        self.assertIn('Email doesnt belong to any user', response.content)

    def test_signup_submit_same_email(self):
        response = self.c.post(
            '/accounts/signup/?code=%s' % self.i.activation_code,
            {
                'username': 'don',
                'first_name': 'wrigley',
                'last_name': 'piggly',
                'email': 'test@test.test',
                'password': 'test',
                'password2': 'test',
            }
        )
        self.assertIn('Email exists on other user', response.content)

    def test_invite_submit_same_email(self):
        my_admin = User.objects.create_superuser('test', 'myemail@test.com', 'test')
        self.c.login(username='test', password='test')
        response = self.c.post(
            '/accounts/invite/',
            {
                u'form-MAX_NUM_FORMS': [u''],
                u'form-0-email': [u'test@test.test'],
                u'form-TOTAL_FORMS': [u'1'],
                u'form-0-username': [u'bobby'],
                u'form-INITIAL_FORMS': [u'0'],
                u'form-0-last_name': [u'test'],
                u'form-0-first_name': [u'test'],
                u'form-0-greeting': [u'']
            },
        )
        self.assertIn('already belongs to a user', response.content)

    def test_reset_submit(self):
        user = User.objects.create(
            username='django',
            email='1234testemail@noone.ghost',
            password='test',
            first_name='test',
            last_name='test',
        )
        psi = PasswordResetInvitation.objects.create(
            email='1234testemail@noone.ghost',
            username='django',
            first_name='test',
            last_name='test',
        )
        response = self.c.post('/accounts/reset/', {'password': 'test', 'password2': 'pest'})
        self.assertIn('Passwords are not the same', response.content)
        response = self.c.post(
            '/accounts/reset/?reset_code=%s' % psi.activation_code,
            {'password': 'test', 'password2': 'test'},
            follow=True
        )
        self.assertIn('The UNT Digital Library: Dashboard', response.content)

    def test_forgotten_password(self):
        '''user forgets his password test'''
        response = self.c.post('/accounts/amnesia/', {'email': 'test@test.test'}, follow=True)
        pri = PasswordResetInvitation.objects.get(email='test@test.test')
        reset_link = '/accounts/reset/?reset_code=%s' % pri.activation_code
        response = self.c.get(reset_link)
        self.assertIn('Enter your new password', response.content)
        response = self.c.post(reset_link, {'password': 'kookaburra', 'password2': 'kookaburra'}, follow=True)
        self.assertIn('Log Out', response.content)


if __name__ == '__main__':
    unittest.main()
