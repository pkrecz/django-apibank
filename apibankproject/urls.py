# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
                    title="MiniBank API",
                    default_version="v1",
                    description="Portfolio",
                    contact=openapi.Contact(email="pkrecz@poczta.onet.pl"),
                    license=openapi.License(name="BSD License")),
    public=True,
    permission_classes=(permissions.AllowAny,))


urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("favicon.ico/", RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico"))),
    path("admin/", admin.site.urls),
    path("user/", include("userapp.urls")),
    path("", include("apibankapp.urls")),
]
