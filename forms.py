from invite.models import InviteItem
from django import forms
from django.forms import ModelForm, Textarea, TextInput, SelectMultiple, CheckboxInput
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Permission, Group
from django.core import validators
from django.core.exceptions import ValidationError


def validate_username(value):
    if value in User.objects.all().values_list('username', flat=True):
        raise ValidationError('Username taken, choose another')


def validate_user_email(value):
    if value not in User.objects.all().values_list('email', flat=True):
        raise ValidationError('Email doesnt belong to any user')


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
        widget=forms.PasswordInput(attrs=\
            {
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
        widget=forms.PasswordInput(attrs=\
            {
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

    def clean(self, *args, **kwargs):
        self.clean_password()
        return self.cleaned_data


class InviteItemForm(ModelForm):
    username = forms.CharField(
        validators=[validate_username],
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': 'true',
                'class': 'input-medium',
            }
        ),
    )
    email = forms.EmailField(
        validators=[validators.validate_email],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input-medium',
                'required': 'true',
            }
        ),
    )
    class Meta:
        model = InviteItem
        widgets = {
            'greeting': Textarea(
                attrs={
                    'placeholder': 'This optional greeting will be delivered to all recipients.',
                    'style': 'height: 80px; width: 286px; resize: none;',
                }
            ),
            'first_name': TextInput(
                attrs={
                    'placeholder': 'First Name',
                    'class': 'input-medium',
                    'required': 'true',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Last Name',
                    'class': 'input-medium',
                    'required': 'true',
                }
            ),
            'permissions': SelectMultiple(
                attrs={
                    'style': 'height: 150px; width: 300px;',
                },
            ),
            'groups': SelectMultiple(
                attrs={
                    'style': 'height: 80px; width: 300px;',
                }
            ),
            'is_super_user': CheckboxInput(
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
                'style': 'width: 75%',
                'required': 'true',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=\
            {
                'placeholder': 'Password',
                'style': 'width: 75%',
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
        validators=[validate_user_email, validators.validate_email],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'required': 'true',
            }
        ),
    )


class ResetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=\
            {
                'placeholder': 'choose a password',
                'class': 'input-medium',
                'required': 'true',
            }
        ),
        label="Choose a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=\
            {
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