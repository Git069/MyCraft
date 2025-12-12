from rest_framework import serializers
from django.utils import timezone
from .models import Job
# Import ReviewSerializer carefully to avoid circular dependency
# A simple one is better here if needed, or use a string import.
# from reviews.serializers import ReviewSerializer 

class SimpleReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rating = serializers.IntegerField()

class JobSerializer(serializers.ModelSerializer):
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)
    review = SimpleReviewSerializer(read_only=True) # Nest the review if it exists

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'trade', 'zip_code', 'city', 
            'execution_date', 'price', 'status', 'created_at', 'updated_at', 
            'contractor', 'client', 'contractor_username',
            'review' # Add review field
        ]
        read_only_fields = ['contractor', 'client', 'status']

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Der Preis darf nicht negativ sein.")
        return value

    def validate_execution_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Das Ausführungsdatum darf nicht in der Vergangenheit liegen.")
        return value

    def validate(self, data):
        if self.instance and self.instance.status != Job.Status.OPEN:
            raise serializers.ValidationError("Nur offene Aufträge können bearbeitet werden.")
        return data
