from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from django.utils import timezone
from .models import Job, Booking

class SimpleReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rating = serializers.IntegerField()

class JobSerializer(GeoFeatureModelSerializer):
    """
    Serializer for the Service (Job) model, now with GeoJSON support.
    """
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)
    review = SimpleReviewSerializer(read_only=True, required=False)

    class Meta:
        model = Job
        geo_field = "location" # Specify the geometry field
        fields = [
            'id', 'title', 'description', 'trade', 'address', 
            'execution_date', 'price', 'status', 'created_at', 'updated_at', 
            'contractor', 'contractor_username', 'review'
        ]
        read_only_fields = ['contractor', 'status']

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
            raise serializers.ValidationError("Nur offene Inserate können bearbeitet werden.")
        return data

class BookingSerializer(serializers.ModelSerializer):
    service = JobSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'customer', 'customer_name', 'contractor', 'status', 'price', 'scheduled_date', 'created_at']
        read_only_fields = ['customer', 'contractor']
