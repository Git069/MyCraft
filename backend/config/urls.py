from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.urls import router as user_router
from .views import api_root

urlpatterns = [
    # Root API endpoint
    path('', api_root, name='api-root'),

    # Admin interface
    path("admin/", admin.site.urls),

    # Authentication and User Management
    path('api/auth/', include(user_router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('users.urls')),

    # Application APIs
    path("api/", include("jobs.urls")),
    path("api/", include("chat.urls")),
    path("api/", include("reviews.urls")),
]

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
