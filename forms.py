from invite.models import InviteItem
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError


def validate_username(value):
    if value in User.objects.all().values_list('username', flat=True):
        raise ValidationError('Username taken, choose another')


def validate_user_email(value):
    insensitive_emails = (
        [e.lower() for e in User.objects.all().values_list('email', flat=True)]
    )
    assert False, insensitive_emails
    if value.lower() not in insensitive_emails:
        raise ValidationError('The email provided doesn\'t belong to any user')


def validate_user_email_exists(value):
    if value in User.objects.all().values_list('email', flat=True):
        raise ValidationError(
            'The email provided: \'%s\' already belongs to a user' % value)


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '1',
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '2',
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '3',
            }
        ),
    )
    username = forms.CharField(
        validators=[validate_username],
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '4',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'choose a password',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '5',
            }
        ),
        label="Choose a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'repeat password',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
                'tabindex': '6',
            }
        ),
        label="Repeat your password"
    )

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean_email(self):
        user_emails = User.objects.all().values_list('email', flat=True)
        if self.data['email'] in user_emails:
            raise forms.ValidationError('Email exists on other user')
        return self.data['email']

    def clean(self, *args, **kwargs):
        self.clean_password()
        self.clean_email()
        return self.cleaned_data


class InviteItemForm(forms.ModelForm):
    # Construct group choices list because many to many fields do not have
    # an order

    username = forms.CharField(
        validators=[validate_username],
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'onkeydown': 'if (event.keyCode == 13) { this.form.submit(); return false; }',
                'placeholder': 'Username',
                'required': 'true',
                'class': 'input-medium',
            }
        ),
    )
    email = forms.EmailField(
        validators=[validators.validate_email, validate_user_email_exists],
        widget=forms.TextInput(
            attrs={
                'onkeydown': 'if (event.keyCode == 13) { this.form.submit(); return false; }',
                'placeholder': 'Email',
                'class': 'input-medium',
                'required': 'true',
            }
        ),
    )

    class Meta:
        model = InviteItem
        widgets = {
            'greeting': forms.Textarea(
                attrs={
                    'placeholder': 'This optional greeting will be delivered to all recipients.',
                    'style': 'height: 80px; width: 286px; resize: none;',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'onkeydown': 'if (event.keyCode == 13) { this.form.submit(); return false; }',
                    'placeholder': 'First Name',
                    'class': 'input-medium',
                    'required': 'true',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'onkeydown': 'if (event.keyCode == 13) { this.form.submit(); return false; }',
                    'placeholder': 'Last Name',
                    'class': 'input-medium',
                    'required': 'true',
                }
            ),
            'permissions': forms.SelectMultiple(
                attrs={
                    'style': 'height: 150px; width: 300px;',
                },
            ),
            'groups': forms.SelectMultiple(
                attrs={
                    'style': 'height: 150px; width: 300px;',
                },
            ),
            'is_super_user': forms.CheckboxInput(
                attrs={
                    'class': 'span1',
                }
            )
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'style': 'width: 75%;',
                'required': 'true',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'style': 'width: 75%;',
                'required': 'true',
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username:
            raise forms.ValidationError("Fill in a username")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data


class IForgotForm(forms.Form):
    email = forms.EmailField(
        validators=[validators.validate_email],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': 'true',
            }
        ),
    )

    def clean_email(self):
        insensitive_emails = [e.lower() for e in User.objects.all().values_list('email', flat=True)]
        if self.data['email'].lower() not in insensitive_emails:
            raise ValidationError(
                'The email provided doesn\'t belong to any user')
        return self.data['email']

    def clean(self, *args, **kwargs):
        self.clean_email()
        return self.cleaned_data


class ResetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'choose a password',
                'class': 'input-medium',
                'required': 'true',
            }
        ),
        label="Choose a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'repeat password',
                'class': 'input-medium',
                'required': 'true',
            }
        ),
        label="Repeat your password"
    )

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_password()
        return self.cleaned_data
