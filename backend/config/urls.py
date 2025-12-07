"""
URL configuration for the MyCraft project.
"""

from django.contrib import admin
from django.urls import path, include
from .views import api_root  # Import the new view

urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),

    # Admin Site
    path("admin/", admin.site.urls),

    # App-specific URLs
    path("api/auth/", include("users.urls")),
    path("api/", include("jobs.urls")),
]
