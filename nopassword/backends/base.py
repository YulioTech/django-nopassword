# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import FieldError

from nopassword.models import LoginCode
from nopassword.utils import get_user_model


class NoPasswordBackend(ModelBackend):
    def authenticate(self, code=None, **credentials):
        try:
            print "credentials = %s" % (str(credentials))
            if "password" in credentials:
                return None
            user = get_user_model().objects.get(**credentials)
        except  get_user_model().DoesNotExist:
            if getattr(settings, 'NOPASSWORD_CREATE_USERS', False):
                user = self.create_user(**credentials)
                if not user:
                    return None
            else:
                return None
        try:
            if not self.verify_user(user):
                return None
            if code is None:
                return LoginCode.create_code_for_user(user)
            else:
                timeout = getattr(settings, 'NOPASSWORD_LOGIN_CODE_TIMEOUT', 900)
                timestamp = datetime.now() - timedelta(seconds=timeout)
                login_code = LoginCode.objects.get(user=user, code=code, timestamp__gt=timestamp)
                user = login_code.user
                user.code = login_code
                multiuse_logins = getattr(settings, 'NOPASSWORD_MULTIUSE_CODES', False)
                if (not multiuse_logins):
                    login_code.delete()
                return user
        except (TypeError, get_user_model().DoesNotExist, LoginCode.DoesNotExist, FieldError):
            return None

    def create_user(self):
        return None

    def send_login_code(self, code, secure=False, host=None, **kwargs):
        raise NotImplementedError

    def verify_user(self, user):
        return user.is_active
