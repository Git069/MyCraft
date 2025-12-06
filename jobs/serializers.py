from rest_framework import serializers
from .models import Job
from django.contrib.auth.models import User


class JobSerializer(serializers.ModelSerializer):
    """
    Wandelt Job-Models in JSON um und validiert eingehende Daten.
    """

    # Optional: Fügt den Benutzernamen des Handwerkers hinzu (nur lesbar).
    # Das ist hilfreich für das Frontend, um nicht nur die ID (z.B. 5) anzuzeigen.
    contractor_username = serializers.ReadOnlyField(source='contractor.username')

    # Optional: Gibt den lesbaren Text des Status zurück (z.B. "Offen" statt "OPEN")
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    trade_display = serializers.CharField(source='get_trade_display', read_only=True)

    class Meta:
        model = Job
        # '__all__' nimmt alle Felder aus dem Model.
        # Alternativ kannst du eine Liste angeben: ['id', 'title', 'price', ...]
        fields = '__all__'

        # Diese Felder dürfen vom Frontend nicht bearbeitet werden
        read_only_fields = ['created_at', 'updated_at', 'contractor']