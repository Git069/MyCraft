from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BecomeCraftsmanView, ProfilePictureUploadView, CustomUserViewSet, UserProfileUpdateView

# Djoser's router for users, but using our custom viewset
router = DefaultRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path('become-craftsman/', BecomeCraftsmanView.as_view(), name='become-craftsman'),
    path('upload-profile-picture/', ProfilePictureUploadView.as_view(), name='upload-profile-picture'),
    path('update-profile/', UserProfileUpdateView.as_view(), name='update-profile'), # <--- NEU
]
