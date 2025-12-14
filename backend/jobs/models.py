from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Job(models.Model):
    """
    Repräsentiert ein Service-Inserat (Dauer-Angebot).
    """
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Aktiv')
        PAUSED = 'PAUSED', _('Pausiert')
        # BOOKED/COMPLETED removed, as these are now Booking states

    class Trade(models.TextChoices):
        PLUMBER = 'PLUMBER', _('Sanitär & Heizung')
        ELECTRICIAN = 'ELECTRICIAN', _('Elektrik')
        PAINTER = 'PAINTER', _('Maler & Lackierer')
        CARPENTER = 'CARPENTER', _('Tischler & Schreiner')
        GARDENER = 'GARDENER', _('Garten & Landschaftsbau')
        OTHER = 'OTHER', _('Sonstiges')

    title = models.CharField(max_length=100, verbose_name=_("Titel"))
    description = models.TextField(verbose_name=_("Beschreibung"))
    trade = models.CharField(max_length=50, choices=Trade.choices, default=Trade.OTHER, verbose_name=_("Gewerbe"))
    zip_code = models.CharField(max_length=5, verbose_name=_("Postleitzahl"))
    city = models.CharField(max_length=100, verbose_name=_("Stadt"), blank=True)
    
    # Optional: Default availability or price indication
    execution_date = models.DateField(null=True, blank=True, verbose_name=_("Verfügbar ab"))
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Startpreis (€)"))

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offered_services', verbose_name=_("Handwerker"))
    
    # Client field removed from Job, as multiple clients can book one service via Booking model

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Booking(models.Model):
    """
    Repräsentiert eine konkrete Buchung eines Services.
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
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Vereinbarter Preis"))
    scheduled_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.id} for {self.service.title}"
