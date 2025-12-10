"""
URL configuration for the MyCraft project.
"""

from django.contrib import admin
from django.urls import path, include
from .views import api_root

urlpatterns = [
    # API Root
    path('', api_root, name='api-root'),

    # Admin Site
    path("admin/", admin.site.urls),

    # Djoser Auth URLs
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),

    # App-specific URLs
    path("api/", include("jobs.urls")),
]
