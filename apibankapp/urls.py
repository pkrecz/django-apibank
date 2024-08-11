# -*- coding: utf-8 -*-

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from .views import (CustomerViewSet, AccountViewSet, AccountTypeViewSet, ParameterViewSet, LogViewSet)


router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'account', AccountViewSet)
router.register(r'accounttype', AccountTypeViewSet)
router.register(r'parameter', ParameterViewSet)
router.register(r'monitoring', LogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
