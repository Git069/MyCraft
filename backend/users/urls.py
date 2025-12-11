from django.urls import path
from .views import BecomeCraftsmanView, ProfilePictureUploadView

urlpatterns = [
    path('become-craftsman/', BecomeCraftsmanView.as_view(), name='become-craftsman'),
    path('upload-profile-picture/', ProfilePictureUploadView.as_view(), name='upload-profile-picture'),
]
