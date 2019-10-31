# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import AuthenticationForm
from .models import LoginCode
from .utils import get_username, get_username_field


def login(request, *args, **kwargs):
    if request.method == 'GET':
        if request.user.is_authenticated:
            redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
            redirect_to = request.GET.get('next', redirect_to)
            return redirect(redirect_to)
        request.session.set_test_cookie()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            if getattr(settings, 'NOPASSWORD_USE_EMAIL', False):
                code = LoginCode.objects.filter(**{
                    'user__%s' % get_username_field(): request.POST.get('email').lower()
                })[0]
            else:
                code = LoginCode.objects.filter(**{
                    'user__%s' % get_username_field(): request.POST.get('username')
                })[0]
            code.next = request.POST.get('next')
            code.save()
            code.send_login_code(
                secure=request.is_secure(),
                host=request.get_host(),
            )
            return render(request, 'registration/sent_mail.html')

    return DjangoLoginView.as_view()(request, authentication_form=AuthenticationForm)


def login_with_code(request, login_code):
    code = get_object_or_404(LoginCode.objects.select_related('user'), code=login_code)
    return login_with_code_and_username(request, username=get_username(code.user),
                                        login_code=login_code)


def login_with_code_and_username(request, username, login_code):
    code = get_object_or_404(LoginCode, code=login_code)
    login_with_post = getattr(settings, 'NOPASSWORD_POST_REDIRECT', True)

    if request.method == 'POST' or not login_with_post:
        user = authenticate(**{get_username_field(): username, 'code': login_code})
        if user is None:
            raise Http404
        user = auth_login(request, user)
        return redirect(code.__next__)

    return render(request, 'registration/login_submit.html')


def logout(request, redirect_to=None):
    auth_logout(request)
    if redirect_to is None:
        return redirect(reverse('nopassword:login'))
    else:
        return redirect(redirect_to)
