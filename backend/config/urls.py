from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root
from users.urls import router as user_router

urlpatterns = [
    path('', api_root, name='api-root'),
    path("admin/", admin.site.urls),
    
    path('api/auth/', include(user_router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('users.urls')),

    # Renamed from 'jobs.urls' to reflect the new structure
    path("api/", include("jobs.urls")),
    path("api/", include("chat.urls")),
    path("api/", include("reviews.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
