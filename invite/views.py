from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

from . import forms
from .models import Invitation, PasswordResetInvitation
from . import settings as app_settings
from .utils import get_cutoff_date


def reset(request):
    '''users land here to reset their django user passwords'''
    if request.method == 'POST':
        reset_code = request.GET.get('reset_code')
        form = forms.ResetForm(request.POST)
        if form.is_valid():
            # get invitation object so we can deleted it afterwards
            pri = (PasswordResetInvitation
                   .objects
                   .get(activation_code=reset_code))
            # determine user from password reset invitation.
            user = User.objects.get(username=pri.username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            pri.send_confirm(request=request)
            pri.delete()
            user = authenticate(
                username=pri.username,
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                # Redirect to main edit dashboard
                return HttpResponseRedirect(
                    app_settings.INVITE_SIGNUP_SUCCESS_URL)
            else:
                return render(
                    request,
                    'invite/contact.html',
                    {
                        'reset_contact':  app_settings.INVITE_CONTACT_EMAIL,
                    }
                )
        else:
            return render(
                request,
                'invite/reset.html',
                {
                    'resetform': form,
                    'reset_code': reset_code,
                }
            )
    elif request.method == 'GET':
        # they come bearing a reset_code
        if 'reset_code' in request.GET.keys():
            try:
                pri = PasswordResetInvitation.objects.get(
                    activation_code=request.GET.get('reset_code'))
            except PasswordResetInvitation.DoesNotExist:
                return render(
                    request,
                    'invite/denied.html'
                )
            return render(
                request,
                'invite/reset.html',
                {
                    'reset_code': pri.activation_code,
                    'resetform': forms.ResetForm(),
                }
            )
        # or an email address
        elif 'email' in request.GET.keys():
            return render(
                request,
                'invite/confirm_reset.html',
                {
                    'email': request.GET.get('email'),
                    'resetform': forms.ResetForm(),
                }
            )
        # otherwise tell em to scram
        else:
            return render(
                request,
                'invite/index.html',
                {
                    'resetform': forms.ResetForm(),
                }
            )


def amnesia(request):
    # iforgot form.
    if request.method == 'POST':
        form = forms.IForgotForm(request.POST)
        if form.is_valid():
            # determine user from email address.
            user = User.objects.filter(email__iexact=form.cleaned_data['email']).first()
            if user.is_active:
                # make password reset invitation from form
                i = PasswordResetInvitation.objects.create(
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                    email=form.cleaned_data['email'],
                )
                # send the email reset link
                i.send(request=request)
                i.save()
                redirect = '{0}?email={1}'.format(
                    reverse('invite:reset'),
                    form.cleaned_data['email'])
                return HttpResponseRedirect(redirect)
            else:
                return render(
                    request,
                    'invite/contact.html',
                    {
                        'reset_contact':  app_settings.INVITE_CONTACT_EMAIL,
                    }
                )
        else:
            return render(
                request,
                'invite/amnesia.html',
                {'iforgotform': form}
            )
    else:
        return render(
            request,
            'invite/amnesia.html',
            {'iforgotform': forms.IForgotForm()}
        )


@csrf_protect
def log_out_user(request):
    logout(request)
    # redirect on logout to root
    return HttpResponseRedirect(app_settings.INVITE_LOGOUT_REDIRECT_URL)


@csrf_protect
def log_in_user(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to next page.
                    return HttpResponseRedirect(reverse('invite:index'))
    else:
        form = forms.LoginForm()
    return render(
        request,
        'invite/login.html',
        {
            'login_form': form,
        }
    )


@login_required(redirect_field_name=None,
                login_url=reverse_lazy('invite:login'))
def index(request):
    invites = Invitation.objects.all().order_by('-date_invited')
    cutoff_date = get_cutoff_date(app_settings.INVITE_OPEN_INVITE_CUTOFF)
    if cutoff_date is not None:
        # Remove all invitations that took place before that date.
        invites = invites.filter(date_invited__gte=cutoff_date)

    users = User.objects.all().order_by('date_joined')
    cutoff_date = get_cutoff_date(app_settings.INVITE_REGISTRATION_CUTOFF)
    if cutoff_date is not None:
        # Remove all registrations that took place before that date.
        users = users.filter(date_joined__gte=cutoff_date)

    return render(
        request,
        'invite/index.html',
        {
            'invites': invites,
            'users': users,
            'show_emails': app_settings.INVITE_SHOW_EMAILS,
        }
    )


@login_required(redirect_field_name=None,
                login_url=reverse_lazy('invite:login'))
def resend(request, code):
    # if we can't get an object with the code provided, deny them
    try:
        i = Invitation.objects.get(activation_code=code)
    except Invitation.DoesNotExist:
        return render(
            request,
            'invite/denied.html'
        )
    i.send(request=request)
    resent_user = '%s %s' % (i.first_name, i.last_name)

    invites = Invitation.objects.all().order_by('-date_invited')
    cutoff_date = get_cutoff_date(app_settings.INVITE_OPEN_INVITE_CUTOFF)
    if cutoff_date is not None:
        # Remove all invitations that took place before that date.
        invites = invites.filter(date_invited__gte=cutoff_date)

    users = User.objects.all().order_by('date_joined')
    cutoff_date = get_cutoff_date(app_settings.INVITE_REGISTRATION_CUTOFF)
    if cutoff_date is not None:
        # Remove all registrations that took place before that date.
        users = users.filter(date_joined__gte=cutoff_date)

    return render(
        request,
        'invite/index.html',
        {
            'invites': invites,
            'resent_user': resent_user,
            'users': users,
            'show_emails': app_settings.INVITE_SHOW_EMAILS,
        }
    )


@login_required(redirect_field_name=None,
                login_url=reverse_lazy('invite:login'))
def revoke(request, code):
    # if we can't get an object with the code provided, deny them
    try:
        i = Invitation.objects.get(activation_code=code)
    except Invitation.DoesNotExist:
        return render(
            request,
            'invite/denied.html'
        )
    i.delete()
    return index(request)


@login_required(redirect_field_name=None,
                login_url=reverse_lazy('invite:login'))
def invite(request):
    InviteItemFormSet = formset_factory(
        forms.InviteItemForm,
        formset=BaseFormSet,
    )
    if request.method == 'POST':
        # Create a formset from the submitted data
        invite_item_formset = InviteItemFormSet(request.POST, request.FILES)
        if invite_item_formset.is_valid():
            for form in invite_item_formset.forms:
                # make invite for each form
                i = Invitation.objects.create(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    is_super_user=form.cleaned_data['is_super_user'],
                )
                i.custom_msg = (
                    invite_item_formset
                    .forms[0]
                    .cleaned_data['greeting']
                )
                # set m2m relationships from initial object creation
                permissions = (
                    invite_item_formset
                    .forms[0]
                    .cleaned_data['permissions']
                )
                groups = (
                    invite_item_formset
                    .forms[0]
                    .cleaned_data['groups']
                )

                for permission in permissions:
                    i.permissions.add(permission)
                for group in groups:
                    i.groups.add(group)
                # send the email invitation
                i.send(request=request)
                i.save()
            return HttpResponseRedirect(reverse('invite:index'))
    else:
        invite_item_formset = InviteItemFormSet()
    return render(
        request,
        'invite/invite.html',
        {
            'invite_item_formset': invite_item_formset,
        }
    )


@login_required(redirect_field_name=None,
                login_url=reverse_lazy('invite:login'))
def about(request):
    return render(
        request,
        'invite/about.html'
    )


@csrf_protect
def signup(request):
    code = request.GET.get('code')
    # if we can't get an object with the code provided, deny the signup
    try:
        i = Invitation.objects.get(activation_code=code)
    except Invitation.DoesNotExist:
        return render(
            request,
            'invite/denied.html'
        )
    # if the form is submitted
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            # add permissions
            for permission in i.permissions.all():
                u.user_permissions.add(permission)
            # add group memberships
            for group in i.groups.all():
                group.user_set.add(u)
            # set superuser status and save
            if i.is_super_user is True:
                u.is_superuser = True
            else:
                u.is_superuser = False
            u.save()
            # delete the invite, no longer valid with the user created
            i.delete()
            # log in the new user immediately
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to edit system.
                    return HttpResponseRedirect(
                        app_settings.INVITE_SIGNUP_SUCCESS_URL)
    else:
        # GET request, just show the form with some initial values
        form = forms.SignupForm(
            initial={
                'first_name': i.first_name,
                'last_name': i.last_name,
                'email': i.email,
                'username': i.username,
            }
        )
    return render(
        request,
        'invite/signup.html',
        {
            'request': request,
            'form': form,
            'service_name': app_settings.get_service_name(request=request),
            'activation_code': code,
        }
    )


@permission_required('invite.add_invitation', raise_exception=True)
def check(request):
    """Check to see if username or email address is taken by a user."""
    if request.GET.get('username', None):
        try:
            User.objects.get(username__iexact=request.GET['username'].strip())
            result = True
        except User.DoesNotExist:
            result = False
    elif request.GET.get('email', None):
        try:
            User.objects.get(email__iexact=request.GET['email'].strip())
            result = True
        except User.DoesNotExist:
            result = False
    else:
        result = False
    return JsonResponse({'taken': result})
