# -*- coding: utf-8 -*-
import django
from django.conf import settings
from django.utils.functional import keep_lazy

if django.VERSION >= (1, 5):
    from django.contrib.auth import get_user_model
    AUTH_USER_MODEL = settings.AUTH_USER_MODEL
    get_user_model = keep_lazy(AUTH_USER_MODEL)(get_user_model)
    get_username_field = keep_lazy(str)(lambda: get_user_model().USERNAME_FIELD)
else:
    from django.contrib.auth.models import User
    AUTH_USER_MODEL = 'auth.User'

    def get_user_model():
        return User

    def get_username_field():
        return 'username'


def get_username(user):
    try:
        return user.get_username()
    except AttributeError:
        return user.username
