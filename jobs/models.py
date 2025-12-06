

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    """
    Repräsentiert ein Angebot oder einen Auftrag, der von einem Handwerker
    erstellt wurde und von Nutzern gebucht werden kann.
    """

    # --- 1. Definition der Auswahlmöglichkeiten (Choices) ---

    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Offen')
        BOOKED = 'BOOKED', _('Gebucht')
        COMPLETED = 'COMPLETED', _('Erledigt')
        CANCELLED = 'CANCELLED', _('Storniert')

    class Trade(models.TextChoices):
        PLUMBER = 'PLUMBER', _('Sanitär & Heizung')
        ELECTRICIAN = 'ELECTRICIAN', _('Elektrik')
        PAINTER = 'PAINTER', _('Maler & Lackierer')
        CARPENTER = 'CARPENTER', _('Tischler & Schreiner')
        GARDENER = 'GARDENER', _('Garten & Landschaftsbau')
        OTHER = 'OTHER', _('Sonstiges')

    # --- 2. Grundlegende Informationen ---

    title = models.CharField(
        max_length=100,
        verbose_name=_("Titel")
    )

    description = models.TextField(
        verbose_name=_("Beschreibung")
    )

    trade = models.CharField(
        max_length=50,
        choices=Trade.choices,
        default=Trade.OTHER,
        verbose_name=_("Gewerbe")
    )

    # --- 3. Ort und Zeit ---

    zip_code = models.CharField(
        max_length=5,
        verbose_name=_("Postleitzahl")
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_("Stadt"),
        blank=True
    )

    # Wann soll der Auftrag ausgeführt werden? (Optional, falls Festtermin)
    execution_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Ausführungsdatum")
    )

    # --- 4. Preisgestaltung (Wichtig für Buchungen) ---

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Preis (€)")
    )

    # --- 5. Status und Metadaten ---

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name=_("Status")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Erstellt am")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Aktualisiert am")
    )

    # --- 6. Verknüpfungen (User) ---

    # Der Handwerker, der das Angebot erstellt hat
    contractor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='offered_jobs',
        verbose_name=_("Handwerker")
    )

    # Der Nutzer, der den Auftrag bucht (erst leer, dann gefüllt)
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booked_jobs',
        verbose_name=_("Kunde")
    )

    class Meta:
        ordering = ['-created_at']  # Neueste Aufträge zuerst
        verbose_name = _("Auftrag")
        verbose_name_plural = _("Aufträge")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"