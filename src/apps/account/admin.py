from django.contrib import admin

from apps.account.models import Account, Contract

admin.site.register(Account)
admin.site.register(Contract)
