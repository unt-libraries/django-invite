from invite.models import * # Change as necessary
from django import forms
from django.forms import ModelForm, Textarea, TextInput, SelectMultiple, CheckboxInput
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login
from django.core import validators


class UserField(forms.CharField):
    def clean(self, value):
        super(UserField, self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError(
                "Name taken. Pick another."
            )
        except User.DoesNotExist:
            return value



class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
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
            }
        ),
    )
    username = UserField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'input-medium',
                'style': 'width: 50%',
                'required': 'true',
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
            'email': TextInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'input-medium',
                    'type': 'email',
                    'required': 'true',
                }
            ),
            'username': TextInput(
                attrs={
                    'placeholder': 'Username',
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
