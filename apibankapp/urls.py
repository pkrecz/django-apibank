# -*- coding: utf-8 -*-

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import CustomerViewSet, AccountViewSet, AccountTypeViewSet, ParameterViewSet, LogViewSet


router = routers.DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customers")
router.register(r"account", AccountViewSet, basename="accounts")
router.register(r"accounttype", AccountTypeViewSet, basename="accounttypes")
router.register(r"parameter", ParameterViewSet, basename="parameters")
router.register(r"monitoring", LogViewSet, basename="monitorings")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
