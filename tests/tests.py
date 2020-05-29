import datetime
import unittest
import json

from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.test import TestCase
from django.contrib.auth.models import User, Group

from invite.models import Invitation, PasswordResetInvitation
from invite import settings as app_settings
from invite.utils import get_cutoff_date

settings.SITE_ID = 1


class TestOperations(TestCase):

    def test_invite_creation(self):
        """Creates an invite and check to see if we can send the email"""
        i = Invitation.objects.create(
            email='joeyliechty@supergreatmail.com',
        )
        i.save()
        self.assertTrue(Invitation.objects.count() > 0)

    @unittest.mock.patch('invite.models.send_mail')
    def test_email_send(self, mock_django_mailer):
        """
        Since we trust the django mailer, and we don't want to do time wasting
        tests that do actual network activity, we'll use mock to ensure that
        the mailer is called with the correct arguments by the model
        """
        i = Invitation.objects.create(
            email='1234testemail@noone.ghost',
            username='test',
            first_name='test',
            last_name='test',
        )

        message = render_to_string(
            'invite/invitation_email.txt',
            {
                'domain': 'example.com',
                'service_name': app_settings.get_service_name(),
                'activation_code': i.activation_code,
                'custom_msg': i.custom_msg,
            }
        )
        i.send()
        mock_django_mailer.assert_called_with(
            'You have been invited to join the {0}'.format(
                app_settings.get_service_name()),
            message,
            app_settings.INVITE_DEFAULT_FROM_EMAIL,
            [i.email],
        )

    @unittest.mock.patch('invite.models.send_mail')
    def test_password_reset_email_send(self, mock_django_mailer):
        """
        Since we trust the django mailer, and we don't want to do time wasting
        tests that do actual network activity, we'll use mock to ensure that
        the mailer is called with the correct arguments by the model
        """
        i = PasswordResetInvitation.objects.create(
            email='1234testemail@noone.ghost',
            username='test',
            first_name='test',
            last_name='test',
        )
        subject = 'Password Reset: {0}'.format(app_settings.get_service_name())
        message = render_to_string(
            'invite/reset_email.txt',
            {
                'first_name': i.first_name,
                'username': i.username,
                'domain': 'example.com',
                'reset_code': i.activation_code,
            }
        )
        i.send()
        mock_django_mailer.assert_called_with(
            subject,
            message,
            app_settings.INVITE_DEFAULT_FROM_EMAIL,
            [i.email],
        )


class TestUtils(TestCase):
    def test_get_cutoff_date_not_positive_ints(self):
        self.assertTrue(get_cutoff_date(None) is None)
        self.assertTrue(get_cutoff_date('not a number') is None)
        self.assertTrue(get_cutoff_date(-5) is None)
        self.assertTrue(get_cutoff_date(-3.2) is None)
        self.assertTrue(get_cutoff_date(5.4) is None)

    def test_get_cutoff_date_positive_ints(self):
        self.assertTrue(isinstance(get_cutoff_date(7), datetime.date))
        self.assertTrue(get_cutoff_date(7) < datetime.date.today())
        self.assertTrue(isinstance(get_cutoff_date(0), datetime.date))
        self.assertTrue(get_cutoff_date(0) > datetime.date.today())


class TestViews(TestCase):
    def setUp(self):
        self.old_date = datetime.date.today() - datetime.timedelta(weeks=2)
        self.normal_user = User.objects.create(
            username='normal',
            email='normal@normal.normal',
            password='normal',
        )
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@superuser.superuser',
            password='superuser'
        )
        self.supertwo = User.objects.create_superuser(
            username='supertwo',
            email='supertwo@supertwo.supertwo',
            password='supertwo'
        )
        self.alpha_invite = Invitation.objects.create(
            username='alpha',
            first_name='alpha',
            last_name='alpha',
            email='alpha@alpha.alpha'
        )
        self.bravo_invite = Invitation.objects.create(
            username='bravo',
            first_name='bravo',
            last_name='bravo',
            email='bravo@bravo.bravo'
        )
        self.user1 = User.objects.create(
            username='user1',
            email='user1@user1.user1',
            password='user1',
        )
        self.dup_user1 = User.objects.create(
            username='dup_user1',
            email='user1@user1.user1',
            password='dup_user1',
        )
        self.inactive_user = User.objects.create(
            username='inactive_user',
            email='inactiveuser@test.test',
            password='inactiveuser',
            is_active=False,
        )

    def test_multiple_email(self):
        """
        Make sure that the multiple email invitation sends to all emails.
        """
        User.objects.create_superuser('test', 'myemail@test.com', 'test')
        self.client.login(username='test', password='test')
        self.client.post(
            reverse('invite:invite'),
            {
                'form-INITIAL_FORMS': ['0'],
                'form-MAX_NUM_FORMS': [''],
                'form-TOTAL_FORMS': ['3'],
                'form-1-username': ['two'],
                'form-1-email': ['two@two.com'],
                'form-1-first_name': ['ieie'],
                'form-1-last_name': ['ueueu'],
                'form-2-email': ['thr@thr.com'],
                'form-2-first_name': ['oiawbeg'],
                'form-2-username': ['three'],
                'form-2-last_name': ['oaweinf'],
                'form-0-email': ['asdf@one.com'],
                'form-0-username': ['one'],
                'form-0-last_name': ['fdsa'],
                'form-0-first_name': ['asdf'],
                'form-0-greeting': [''],
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
        """
        Since we have to do some hacky group ordering chop around stuff,
        let's make sure that the invitation retains the right group.
        """
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

        self.client.login(username='superuser', password='superuser')
        self.client.post(
            reverse('invite:invite'),
            {
                'form-MAX_NUM_FORMS': [''],
                'form-0-email': ['joeyliechty@gmail.com'],
                'form-TOTAL_FORMS': ['1'],
                # archives civil war, boyce ditto, texas general land office
                'form-0-groups': ['2', '4', '1'],
                'form-0-username': ['jejfi'],
                'form-INITIAL_FORMS': ['0'],
                'form-0-last_name': ['a'],
                'form-0-first_name': ['a'],
                'form-0-greeting': ['']
            }
        )
        invite0 = Invitation.objects.get(email='joeyliechty@gmail.com')
        # assert the invitation has the correct groups
        self.assertEqual(invite0.groups.count(), 3)
        self.assertEqual(invite0.groups.all()[0].name, 'UNT Archives')
        self.assertEqual(invite0.groups.all()[1].name, 'Boyce')
        self.assertEqual(invite0.groups.all()[2].name, 'texgen')

    def test_amnesia_unknown_email(self):
        response = self.client.post(
            reverse('invite:amnesia'),
            {'email': 'avowin@test.test'}
        )

        self.assertIn('The email provided', response.content.decode())

    def test_amnesia_inactive_user(self):
        response = self.client.post(
            reverse('invite:amnesia'),
            {'email': 'inactiveuser@test.test'}
        )

        self.assertIn('Your account is inactive.', response.content.decode())

    def test_amnesia_email_submit_case_insensitive(self):
        response = self.client.post(
            reverse('invite:amnesia'),
            {'email': self.user1.email.upper()},
            follow=True
        )

        self.assertIn(
            'An email was sent to {}'.format(self.user1.email.upper()),
            response.content.decode()
        )

    def test_signup_submit_same_email(self):
        url = '{0}?code={1}'.format(
            reverse('invite:account_signup'),
            self.alpha_invite.activation_code
        )

        response = self.client.post(
            url,
            {
                'username': 'alpha',
                'first_name': 'alpha',
                'last_name': 'alpha',
                'email': self.normal_user.email,
                'password': 'alpha',
                'password2': 'alpha',
            }
        )
        self.assertIn('Email exists on other user', response.content.decode())

    def test_invite_submit_same_email(self):
        self.client.login(username='superuser', password='superuser')
        response = self.client.post(
            reverse('invite:invite'),
            {
                'form-MAX_NUM_FORMS': [''],
                'form-0-email': [self.normal_user.email],
                'form-TOTAL_FORMS': ['1'],
                'form-0-username': ['bobby'],
                'form-INITIAL_FORMS': ['0'],
                'form-0-last_name': ['test'],
                'form-0-first_name': ['test'],
                'form-0-greeting': ['']
            },
        )
        self.assertIn('already belongs to a user', response.content.decode())

    def test_reset_submit(self):
        psi = PasswordResetInvitation.objects.create(
            email='normal@normal.normal',
            username='normal',
            first_name='normal',
            last_name='normal',
        )
        response = self.client.post(
            reverse('invite:reset'),
            {'password': 'test', 'password2': 'pest'}
        )

        self.assertIn('Passwords are not the same', response.content.decode())

        url = '{0}?reset_code={1}'.format(
            reverse('invite:reset'),
            psi.activation_code
        )
        response = self.client.post(
            url,
            {'password': 'test', 'password2': 'test'},
            follow=True
        )
        self.assertEqual(200, response.status_code)
        self.assertIn('Log in', response.content.decode())

    def test_reset_with_expired_code(self):
        mock_today = datetime.date.today() - datetime.timedelta(days=2)
        pri = PasswordResetInvitation.objects.create(
            email='inactiveuser@test.test',
            username='inactive_user',
            first_name='normal',
            last_name='user',
        )
        pri.date_invited = mock_today
        pri.save()
        url = '{0}?reset_code={1}'.format(
                reverse('invite:reset'),
                pri.activation_code
        )
        response = self.client.get(url)
        self.assertIn('That is an invalid or expired activation code.', response.content.decode())

    def test_reset_inactive_user(self):
        pri = PasswordResetInvitation.objects.create(
            email='inactiveuser@test.test',
            username='inactive_user',
            first_name='normal',
            last_name='user',
        )
        url = '{0}?reset_code={1}'.format(
            reverse('invite:reset'),
            pri.activation_code
        )
        response = self.client.post(
            url,
            {'password': 'test', 'password2': 'test'},
            follow=True
        )
        assert response.status_code == 200
        self.assertIn(
            'Your account is inactive.', response.content.decode()
        )

    def test_forgotten_password(self):
        """User forgets his password test"""
        response = self.client.post(
            reverse('invite:amnesia'),
            {'email': 'normal@normal.normal'},
            follow=True
        )

        pri = PasswordResetInvitation.objects.get(email='normal@normal.normal')
        reset_link = '{0}?reset_code={1}'.format(
            reverse('invite:reset'), pri.activation_code)

        response = self.client.get(reset_link)
        self.assertIn('Enter your new password', response.content.decode())

        response = self.client.post(
            reset_link,
            {'password': 'kookaburra', 'password2': 'kookaburra'},
            follow=True
        )
        self.assertIn('Log in', response.content.decode())

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_limited_invites(self, mock_settings):
        mock_settings.INVITE_OPEN_INVITE_CUTOFF = 1
        self.bravo_invite.date_invited = self.old_date
        self.bravo_invite.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertIn('alpha', response_content)
        self.assertNotIn('bravo', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_all_invites(self, mock_settings):
        mock_settings.INVITE_OPEN_INVITE_CUTOFF = None
        self.bravo_invite.date_invited = self.old_date
        self.bravo_invite.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertIn('alpha', response_content)
        self.assertIn('bravo', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_no_invites(self, mock_settings):
        mock_settings.INVITE_OPEN_INVITE_CUTOFF = 0
        self.bravo_invite.date_invited = self.old_date
        self.bravo_invite.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertNotIn('alpha', response_content)
        self.assertNotIn('bravo', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_limited_registrations(self, mock_settings):
        mock_settings.INVITE_REGISTRATION_CUTOFF = 1
        self.normal_user.date_joined = self.old_date
        self.normal_user.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertIn('supertwo', response_content)
        self.assertNotIn('normal', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_all_registrations(self, mock_settings):
        mock_settings.INVITE_REGISTRATION_CUTOFF = None
        self.normal_user.date_joined = self.old_date
        self.normal_user.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertIn('supertwo', response_content)
        self.assertIn('normal', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_shows_no_registrations(self, mock_settings):
        mock_settings.INVITE_REGISTRATION_CUTOFF = 0
        self.normal_user.date_joined = self.old_date
        self.normal_user.save()
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertNotIn('supertwo', response_content)
        self.assertNotIn('normal', response_content)

    def test_index_shows_emails_to_superuser(self):
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertIn('normal@normal.normal', response_content)
        self.assertIn('superuser@superuser.superuser', response_content)
        self.assertIn('alpha@alpha.alpha', response_content)
        self.assertIn('bravo@bravo.bravo', response_content)

    def test_index_hides_emails_from_normal_user(self):
        self.client.login(username='normal', password='normal')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertNotIn('normal@normal.normal', response_content)
        self.assertNotIn('superuser@superuser.superuser', response_content)
        self.assertNotIn('alpha@alpha.alpha', response_content)
        self.assertNotIn('bravo@bravo.bravo', response_content)

    @unittest.mock.patch('invite.views.app_settings')
    def test_index_can_hide_all_emails(self, mock_settings):
        mock_settings.INVITE_SHOW_EMAILS = False
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:index'))
        response_content = response.content.decode()
        self.assertNotIn('normal@normal.normal', response_content)
        self.assertNotIn('superuser@superuser.superuser', response_content)
        self.assertNotIn('alpha@alpha.alpha', response_content)
        self.assertNotIn('bravo@bravo.bravo', response_content)

    def test_check_requires_permission(self):
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:check'))
        self.assertTrue(response.status_code == 200)
        self.client.logout()
        self.client.login(username='normal', password='normal')
        response = self.client.get(reverse('invite:check'))
        self.assertTrue(response.status_code == 403)

    def test_check_returns_true_when_taken(self):
        self.client.login(username='superuser', password='superuser')
        taken = (
            {'username': self.normal_user.username},
            {'username': self.supertwo.username},
            {'email': self.normal_user.email},
            {'email': self.supertwo.email},
        )
        for each in taken:
            response = self.client.get(reverse('invite:check'), each)
            self.assertTrue(json.loads(response.content)['taken'])

    def test_check_returns_false_when_not_taken(self):
        self.client.login(username='superuser', password='superuser')
        not_taken = (
            {'username': 'doesnotexist'},
            {'username': ''},
            {'email': 'nothing@nothing.nothing'},
            {'email': 'test@test.test'},
        )
        for each in not_taken:
            response = self.client.get(reverse('invite:check'), each)
            self.assertFalse(json.loads(response.content)['taken'])

    def test_check_returns_false_with_no_args(self):
        self.client.login(username='superuser', password='superuser')
        response = self.client.get(reverse('invite:check'))
        self.assertFalse(json.loads(response.content)['taken'])


if __name__ == '__main__':
    unittest.main()
