# -*- coding: utf8 -*-
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^login-code/(?P<login_code>[a-zA-Z0-9]+)/$',
        views.login_with_code, name='login_with_code'),
    re_path(r'^login-code/(?P<username>[a-zA-Z0-9_@\.-]+)/(?P<login_code>[a-zA-Z0-9]+)/$',
        views.login_with_code_and_username, name='login_with_code_and_username'),
    re_path(r'^logout/$', views.logout, name='logout'),
]
