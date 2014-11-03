from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User, Permission, Group
from django.views.decorators.csrf import csrf_protect

from django.conf import settings
from .forms import SignupForm, InviteItemForm, LoginForm, IForgotForm, ResetForm
from .models import Invitation, PasswordResetInvitation
from . import settings as app_settings
# from edit_auth.views import require_edit_login


def reset(request):
    '''users land here to reset their django user passwords'''
    if request.method == 'POST':
        reset_code = request.GET.get('reset_code')
        form = ResetForm(request.POST)
        if form.is_valid():
            # get invitation object so we can deleted it afterwards
            pri = PasswordResetInvitation.objects.get(activation_code=reset_code)
            # determine user from password reset invitation.
            user = User.objects.get(username=pri.username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            pri.send_confirm()
            pri.delete()
            user = authenticate(
                username=pri.username,
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to main edit dashboard
                    return HttpResponseRedirect(settings.SIGNUP_REDIRECT_PATH)
        else:
            return render_to_response(
                'invite/reset.html',
                {
                    'resetform': form,
                    'reset_code': reset_code,
                },
                context_instance=RequestContext(request)
            )
    elif request.method == 'GET':
        # they come bearing a reset_code
        if 'reset_code' in request.GET.keys():
            try:
                pri = PasswordResetInvitation.objects.get(activation_code=request.GET.get('reset_code'))
            except PasswordResetInvitation.DoesNotExist:
                return render(
                    request,
                    'invite/denied.html',
                    context_instance=RequestContext(request)
                )
            return render_to_response(
                'invite/reset.html',
                {
                    'reset_code': pri.activation_code,
                    'resetform': ResetForm(),
                },
                context_instance=RequestContext(request)
            )
        # or an email address
        elif 'email' in request.GET.keys():
            return render_to_response(
                'invite/confirm_reset.html',
                {
                    'email': request.GET.get('email'),
                    'resetform': ResetForm(),
                },
                context_instance=RequestContext(request)
            )
        # otherwise tell em to scram
        else:
            return render_to_response(
                'invite/index.html',
                {
                    'resetform': ResetForm(),
                },
                context_instance=RequestContext(request)
            )


def amnesia(request):
    # iforgot form.
    if request.method == 'POST':
        form = IForgotForm(request.POST)
        if form.is_valid():
            # determine user from email address.
            user = User.objects.get(email__iexact=form.cleaned_data['email'])
            # make password reset invitation from form
            i = PasswordResetInvitation.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=form.cleaned_data['email'],
            )
            # send the email reset link
            i.send()
            i.save()
            return HttpResponseRedirect('/accounts/reset/?email=%s' % form.cleaned_data['email'])
        else:
            return render_to_response(
                'invite/amnesia.html',
                {'iforgotform': form},
                context_instance=RequestContext(request)
            )
    else:
        return render_to_response(
            'invite/amnesia.html',
            {'iforgotform': IForgotForm()},
            context_instance=RequestContext(request)
        )


@csrf_protect
def log_out_user(request):
    logout(request)
    # redirect on logout to root
    return HttpResponseRedirect(app_settings.INVITE_LOGOUT_REDIRECT_URL)


@csrf_protect
def log_in_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to next page.
                    return HttpResponseRedirect(reverse('index'))
    else:
        form = LoginForm()
    return render(
        request,
        'invite/base.html',
        {
            'login_form': form,
        },
        context_instance=RequestContext(request)
    )


# @require_edit_login
def index(request):
    return render_to_response(
        'invite/index.html',
        {
            'login_form': LoginForm(),
            'invites': Invitation.objects.all().order_by('-date_invited'),
            'users': User.objects.all().order_by('date_joined'),
        },
        context_instance=RequestContext(request)
    )


# @require_edit_login
def resend(request, code):
    # if we can't get an object with the code provided, deny them
    try:
        i = Invitation.objects.get(activation_code=code)
    except Invitation.DoesNotExist:
        return render(
            request,
            'invite/denied.html',
            context_instance=RequestContext(request)
        )
    i.send()
    resent_user = '%s %s' % (i.first_name, i.last_name)
    return render_to_response(
        'invite/index.html',
        {
            'login_form': LoginForm(),
            'invites': Invitation.objects.all(),
            'resent_user': resent_user,
            'users': User.objects.all(),
        },
        context_instance=RequestContext(request)
    )


# @require_edit_login
def revoke(request, code):
    # if we can't get an object with the code provided, deny them
    try:
        i = Invitation.objects.get(activation_code=code)
    except Invitation.DoesNotExist:
        return render(
            request,
            'invite/denied.html',
            context_instance=RequestContext(request)
        )
    revoked_user = '%s %s' % (i.first_name, i.last_name)
    i.delete()
    return index(request)


# @require_edit_login
def invite(request):
    InviteItemFormSet = formset_factory(
        InviteItemForm,
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
                i.custom_msg = invite_item_formset.forms[0].cleaned_data['greeting']
                # set m2m relationships from initial object creation
                for permission in invite_item_formset.forms[0].cleaned_data['permissions']:
                    i.permissions.add(permission)
                for group in invite_item_formset.forms[0].cleaned_data['groups']:
                    i.groups.add(group)
                # send the email invitation
                i.send()
                i.save()
            return HttpResponseRedirect('/accounts/')
    else:
        invite_item_formset = InviteItemFormSet()
    return render_to_response(
        'invite/invite.html',
        {
            'login_form': LoginForm(),
            'invite_item_formset': invite_item_formset,
        },
        context_instance=RequestContext(request),
    )


def about(request):
    return render(
        request,
        'invite/about.html',
        {'login_form': LoginForm()},
        context_instance=RequestContext(request)
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
            'invite/denied.html',
            context_instance=RequestContext(request)
        )
    # if the form is submitted
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            u.first_name=form.cleaned_data['first_name']
            u.last_name=form.cleaned_data['last_name']
            # add permissions
            for permission in i.permissions.all():
                u.user_permissions.add(permission)
            # add group memberships
            for group in i.groups.all():
                group.user_set.add(u)
            #set superuser status and save
            if i.is_super_user == True:
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
                    return HttpResponseRedirect(settings.SIGNUP_REDIRECT_PATH)
    else:
        # GET request, just show the form with some initial values
        form = SignupForm(
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
            'service_name': settings.SERVICE_NAME,
            'activation_code': code,
        },
        context_instance=RequestContext(request)
    )
