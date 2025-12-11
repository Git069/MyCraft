from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path("admin/", admin.site.urls),
    path('api/auth/', include('users.urls')), 
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path("api/", include("jobs.urls")),
    path("api/", include("chat.urls")),
]

# --- Add this for serving media files in development ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
