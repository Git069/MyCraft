# jobs/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet

# Der Router erstellt automatisch URLs
router = DefaultRouter()
router.register(r'jobs', JobViewSet)

urlpatterns = [
    path('', include(router.urls)),
]