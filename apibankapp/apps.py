# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ApibankappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apibankapp"

    def ready(self):
        import apibankapp.initdata
