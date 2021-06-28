from django.contrib import admin
from wsite.models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
  list_display = ('user', 'contact', 'status')

# Register your models here.
admin.site.register(UserInfo, UserInfoAdmin)