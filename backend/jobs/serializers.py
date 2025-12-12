from rest_framework import serializers
from django.utils import timezone
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'trade', 'zip_code', 'city', 
            'execution_date', 'price', 'status', 'created_at', 'updated_at', 
            'contractor', 'client', 'contractor_username'
        ]
        read_only_fields = ['contractor', 'client']

    def validate_price(self, value):
        """
        Regel 2: Das Budget/Preis darf nicht negativ sein.
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("Der Preis darf nicht negativ sein.")
        return value

    def validate_execution_date(self, value):
        """
        Regel 1: Das Startdatum darf nicht in der Vergangenheit liegen.
        """
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Das Ausführungsdatum darf nicht in der Vergangenheit liegen.")
        return value
