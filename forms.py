from django import forms
from django.contrib.auth.models import User
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


class InviteForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    user_name = UserField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    custom_msg = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'You can write an optional custom greeting here',
                'class': 'block',
                'style': 'display: block; width: 96%',
            }
        ),
    )
    can_invite = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )
    is_super_user = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )

    def clean(self, *args, **kwargs):
        return super(InviteForm, self).clean(*args, **kwargs)


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    user_name = UserField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'input-medium',
                'style': 'width: 45%',
            }
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs=\
            {'placeholder': 'choose a password', 'class': 'input-medium',}
        ),
        label="Choose a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=\
            {'placeholder': 'repeat password', 'class': 'input-medium',}
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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username:
            raise forms.ValidationError("Fill in a username")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username or password")
        return self.cleaned_data
