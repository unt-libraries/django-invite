from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core import validators

PERMISSION_CHOICES = (
    (1, 'Can Invite Users',),
    (3, 'Is SuperUser',),
)


class UserField(forms.CharField):
    def clean(self, value):
        super(UserField, self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError(
                "Someone is already using this username. Please pick another."
            )
        except User.DoesNotExist:
            return value


class InviteForm(forms.Form):
    first_name = forms.CharField(max_length=30, help_text='First Name')
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    user_name = UserField(max_length=30)
    custom_msg = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )
    can_invite = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )
    is_super_user = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
    )

    def clean(self,*args, **kwargs):
        return super(InviteForm, self).clean(*args, **kwargs)


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'input-small'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'input-small'})
    )
    user_name = UserField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'input-large'}),
    )
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Choose a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Repeat your password"
    )

    def clean_first_last(self):
        if not self.data['first_name'] or not self.data['last_name']:
            raise forms.ValidationError('Missing input')

    def clean_email(self):
        if not self.data['email']:
            raise forms.ValidationError('Missing input')

    def clean_username(self):
        if not self.data['user_name']:
            raise forms.ValidationError('Missing input')


    def clean_password(self):
        if not self.data['password'] or not self.data['password2']:
            raise forms.ValidationError('Missing input')
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self,*args, **kwargs):
        self.clean_password()
        self.clean_first_last()
        self.clean_email()
        self.clean_username()
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
