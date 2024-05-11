from django.contrib import admin
from .models import CustomerModel, AccountModel, AccountTypeModel, ParameterModel

admin.site.register(CustomerModel)
admin.site.register(AccountModel)
admin.site.register(AccountTypeModel)
admin.site.register(ParameterModel)

