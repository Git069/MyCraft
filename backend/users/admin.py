"""Admin configuration for the Users application.

This module customizes the Django admin interface for the User model,
adding an inline display for the associated Profile model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """Inline admin descriptor for the Profile model.

    Allows editing the user's profile directly within the User admin page.
    """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


# Unregister the default User admin
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin that displays more information in the list view.

    Extends the base UserAdmin to include the ProfileInline and customize
    list display, filtering, and search capabilities.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    inlines = (ProfileInline,)
