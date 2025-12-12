from rest_framework.routers import DefaultRouter
from .views import JobViewSet, BookingViewSet

router = DefaultRouter()
# Renaming 'jobs' to 'services' for clarity
router.register(r'services', JobViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls
