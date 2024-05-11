# -*- coding: utf-8 -*-

from django.urls import path, include
from rest_framework import routers
from .views import CustomerViewSet, AccountViewSet, AccountTypeViewSet, ParameterViewSet


router = routers.DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'account', AccountViewSet)
router.register(r'accounttype', AccountTypeViewSet)
router.register(r'parameter', ParameterViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
]
