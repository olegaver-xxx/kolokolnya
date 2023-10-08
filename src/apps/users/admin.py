from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class EmailUserAdmin(UserAdmin):
    readonly_fields = ['last_login', 'date_joined']
    list_display = ('email', 'is_active', 'is_staff')
    fieldsets = (
        ('Auth', {'fields': ('email', 'full_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
