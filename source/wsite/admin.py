from django.contrib import admin
from wsite.models import admin_accounts, user_accounts

# Register your models here.
admin.site.register(admin_accounts)
admin.site.register(user_accounts)