from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root
from users.urls import router as user_router # Import our custom router

urlpatterns = [
    path('', api_root, name='api-root'),
    path("admin/", admin.site.urls),
    
    # --- AUTH & USER URLS ---
    # Use our custom router for users, which overrides Djoser's default
    path('api/auth/', include(user_router.urls)),
    
    # Include other specific auth paths
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('users.urls')), # For become-craftsman etc.

    # App-specific URLs
    path("api/", include("jobs.urls")),
    path("api/", include("chat.urls")),
    path("api/", include("reviews.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
