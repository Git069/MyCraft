"""URL configuration for the Users application.

This module defines the URL patterns for user-related views, including
custom Djoser user management, profile updates, and craftsman application.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BecomeCraftsmanView,
    CustomUserViewSet,
    ProfilePictureUploadView,
    UserProfileUpdateView,
)

# Djoser's router for users, but using our custom viewset
router = DefaultRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path('become-craftsman/', BecomeCraftsmanView.as_view(), name='become-craftsman'),
    path('upload-profile-picture/', ProfilePictureUploadView.as_view(), name='upload-profile-picture'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'),
]
