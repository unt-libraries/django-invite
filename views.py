from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Invitation
from .forms import SignupForm, LoginForm, InviteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


def log_out_user(request):
    logout(request)
    # Redirect to a success page.
    return render_to_response(
        'invite/logout.html',
        context_instance=RequestContext(request)
    )


def about(request):
    return render(
        request,
        'invite/about.html',
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
                    # Redirect to a success page.
                    return HttpResponseRedirect('/accounts/')
    else:
        form = LoginForm()
    return render(
        request,
        'invite/login.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def index(request):
    if request.GET.get('next'):
        return HttpResponseRedirect(next)
    return render_to_response(
        'invite/index.html',
        {
            'invites': Invitation.objects.all(),
            'users': User.objects.all(),
        },
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def invite(request):
    if request.method == 'POST':
        form = InviteForm(request.POST)
        if form.is_valid():
            permission_code = 0
            if len(form.cleaned_data['permissions']) > 0:
                permission_code = ''.join(form.cleaned_data['permissions'])
            i = Invitation.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_name=form.cleaned_data['user_name'],
                email=form.cleaned_data['email'],
                permissions=permission_code,
            )
            i.send()
            return HttpResponseRedirect('/accounts/')
    else:
        form = InviteForm()
    return render(
        request,
        'invite/invite.html',
        {
            'form': form,
        },
        context_instance=RequestContext(request)
    )


def signup(request):
    code = request.GET.get('code')
    i = Invitation.objects.filter(activation_code__exact=code)
    if i:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                u = User.objects.create_user(
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    username=form.cleaned_data['user_name'],
                    email=form.cleaned_data['email'],
                )
                u.set_password(form.cleaned_data['password'])
                # add permissions
                for permission in list(i[0].permissions):
                    if permission == '1':
                        content_type = ContentType.objects.get_for_model(Invitation)
                        p = Permission.objects.get(
                            content_type=content_type,
                            codename='add_invitation'
                        )
                        u.user_permissions.add(p)
                    # if permission == '2':
                    #     content_type = ContentType.objects.get_for_model(User)
                    #     p = Permission.objects.get(content_type=content_type, codename='delete_user')
                    #     u.user_permissions.add(p)
                    elif permission == '3':
                        u.is_superuser = True
                u.save()
                # delete the invite
                i[0].delete()
                return HttpResponseRedirect('/accounts/')
        else:
            form = SignupForm(
                initial={
                    'first_name': i[0].first_name,
                    'last_name': i[0].last_name,
                    'email': i[0].email,
                    'user_name': i[0].user_name,
                }
            )
        return render(
            request,
            'invite/signup.html',
            {
                'form': form,
                'activation_code': code,
            },
            context_instance=RequestContext(request)
        )
    else:
        return render(
            request,
            'invite/denied.html',
            context_instance=RequestContext(request)
        )


def send(request):
    i = Invitation.objects.create(email=request.GET.get('email'))
    i.send()
    return render(request, 'invite/sent.html')
