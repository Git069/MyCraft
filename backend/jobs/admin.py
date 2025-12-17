from django.contrib.gis import admin
from .models import Job, Booking

@admin.register(Job)
class JobAdmin(admin.OSMGeoAdmin):
    """
    Admin view for Services (Jobs) with OpenStreetMap integration.
    """
    list_display = ('title', 'contractor', 'status', 'created_at')
    list_filter = ('status', 'trade')
    search_fields = ('title', 'description', 'city')
    
    # Configure the map
    default_lon = 10.4515 # Center of Germany
    default_lat = 51.1657
    default_zoom = 6

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer', 'contractor', 'status', 'price', 'created_at')
    list_filter = ('status',)
    search_fields = ('service__title', 'customer__username', 'contractor__username')
