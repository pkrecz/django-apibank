# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import logout_view, register_view, change_password


urlpatterns = [
    path(route='login/', view=obtain_auth_token, name='login'),
    path(route='logout/', view=logout_view, name='logout'),
    path(route='register/', view=register_view, name='register'),
    path(route='change-password/', view=change_password, name='change-password'),
]
