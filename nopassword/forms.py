# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.core.validators import validate_email

from .models import LoginCode
from .utils import get_username_field


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username logins.
    """
    if getattr(settings, 'NOPASSWORD_USE_EMAIL', False):
        email = forms.EmailField(label=_("Email"),
                    required=True,
                    max_length=150,
                    widget=forms.EmailInput(attrs={'class':'form-control'}))
        invalid_login = _("That email address doesn't exist, please enter a correct email address.")
    else:
        username = forms.CharField(label=_("Username"), required=True, max_length=30)
        invalid_login = _("Please enter a correct username. "
                           "Note that both fields are case-sensitive."),

    error_messages = {
        'invalid_login': invalid_login,
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        if not getattr(settings, 'NOPASSWORD_USE_EMAIL', False):
            self.fields['username'].label = _(get_username_field().capitalize())

    def clean(self):
        if getattr(settings, 'NOPASSWORD_USE_EMAIL', False):
            email = self.cleaned_data.get('email')
            self.user_cache = authenticate(**{'email': email})
        else:
            username = self.cleaned_data.get('username')
            self.user_cache = authenticate(**{get_username_field(): username})
        if self.user_cache is None:
            raise forms.ValidationError(self.error_messages['invalid_login'])
        elif not isinstance(self.user_cache, LoginCode) and \
                not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])

        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
