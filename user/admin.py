from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'account', 'password', 'authority']


admin.site.register(User, UserAdmin)
