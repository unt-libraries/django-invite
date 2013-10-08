from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Permission
import settings
from .forms import SignupForm, InviteItemForm, LoginForm
from .models import Invitation
from django.contrib.auth.models import User, Permission, Group


def log_out_user(request):
    logout(request)
    # Redirect to a success page.
    return render_to_response(
        'invite/base.html',
        {'login_form': LoginForm()},
        context_instance=RequestContext(request)
    )


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
                    return HttpResponseRedirect('/accounts/')
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


def resend(request, code):
    i = Invitation.objects.filter(activation_code__exact=code)
    i[0].send()
    return HttpResponseRedirect('/accounts/')

def revoke(request, code):
    i = Invitation.objects.filter(activation_code__exact=code)
    i[0].delete()
    return HttpResponseRedirect('/accounts/')


def invite(request):
    InviteItemFormSet = formset_factory(
        InviteItemForm,
        formset=BaseFormSet
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
                # set m2m relationships from initial object creation
                for permission in invite_item_formset.forms[0].cleaned_data['permissions']:
                    i.permissions.add(permission)
                for group in invite_item_formset.forms[0].cleaned_data['groups']:
                    i.groups.add(group)
                # send the email invitation
                i.send()
                i.save()
            return HttpResponseRedirect('/accounts/') # Redirect to a 'success' page
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

def pizza(request):
    return render(
        request,
        'invite/pizza.html',
        {},
        context_instance=RequestContext(request)
    )


def index(request):
    return render_to_response(
        'invite/index.html',
        {
            'login_form': LoginForm(),
            'invites': Invitation.objects.all(),
            'users': User.objects.all(),
        },
        context_instance=RequestContext(request)
    )


def signup(request):
    code = request.GET.get('code')
    # if we can't get an object with the code provided, deny the signup
    try:
        i = Invitation.objects.get(activation_code=code)
    except Exception, e:
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
                    # Redirect to accounts page.
                    return HttpResponseRedirect('/accounts/')
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

