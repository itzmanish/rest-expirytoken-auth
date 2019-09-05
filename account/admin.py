from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'name', 'is_admin', 'avatar')
    search_fields = ('username', 'is_admin',)
    list_filter = ('is_admin',)
    ordering = ('username', 'email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'name', 'password', 'avatar')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_staff')})
    )

    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
