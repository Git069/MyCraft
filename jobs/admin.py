from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Zeigt diese Spalten in der Listenansicht an
    list_display = ('title', 'contractor', 'trade', 'price', 'status', 'created_at')

    # Fügt Filter in der Seitenleiste hinzu
    list_filter = ('status', 'trade', 'created_at')

    # Ermöglicht die Suche nach Titel oder Beschreibung
    search_fields = ('title', 'description')