"""App configuration for the Users application."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the Users application.

    Sets the default auto field type and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
