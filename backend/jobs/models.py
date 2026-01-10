from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point

class Job(models.Model):
    """
    Represents a Service listing.
    """
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Aktiv')
        PAUSED = 'PAUSED', _('Pausiert')

    class Trade(models.TextChoices):
        PLUMBER = 'PLUMBER', _('Sanitär & Heizung')
        ELECTRICIAN = 'ELECTRICIAN', _('Elektrik')
        PAINTER = 'PAINTER', _('Maler & Lackierer')
        CARPENTER = 'CARPENTER', _('Tischler & Schreiner')
        GARDENER = 'GARDENER', _('Garten & Landschaftsbau')
        OTHER = 'OTHER', _('Sonstiges')

    title = models.CharField(max_length=100)
    description = models.TextField()
    trade = models.CharField(max_length=50, choices=Trade.choices, default=Trade.OTHER)
    
    # --- NEW & UPDATED GEO FIELDS ---
    address = models.CharField(max_length=255, blank=True)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    
    # Old location fields are now deprecated but kept for now to avoid breaking old code
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=100, blank=True)

    execution_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offered_services')

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Nur geocoden, wenn Location fehlt UND Adressdaten da sind
        # WICHTIG: Wir prüfen auch, ob sich die Adresse geändert hat (optional für später)
        if not self.location and (self.address or (self.city and self.zip_code)):
            try:
                # User Agent sollte einzigartig für dein Projekt sein
                geolocator = Nominatim(user_agent="mycraft_backend_app_prod")

                query = f"{self.address}, {self.zip_code} {self.city}"

                # Timeout erhöhen, da Nominatim manchmal langsam ist
                loc = geolocator.geocode(query, timeout=10)

                if loc:
                    self.location = Point(loc.longitude, loc.latitude)
                else:
                    print(f"GEOCODING WARNING: Keine Koordinaten gefunden für '{query}'")
            except Exception as e:
                # Hier könnte man auch logging.error() nutzen
                print(f"GEOCODING ERROR: {e}")

        super().save(*args, **kwargs)

class Booking(models.Model):
    """
    Represents a concrete booking of a Service.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Ausstehend')
        CONFIRMED = 'CONFIRMED', _('Bestätigt')
        COMPLETED = 'COMPLETED', _('Erledigt')
        CANCELLED = 'CANCELLED', _('Storniert')

    service = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_received')
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    scheduled_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.id} for {self.service.title}"
