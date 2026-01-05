from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Job, Booking


class JobSerializer(serializers.ModelSerializer):
    # Wir fügen zwei "Schreib-Felder" hinzu, die nicht in der DB, aber im Input existieren
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('contractor', 'created_at', 'status',
                            'location')  # location ist read-only, wird via lat/lng gesetzt

    def create(self, validated_data):
        # Koordinaten aus den Daten holen (und entfernen, da sie nicht im Model existieren)
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        # Wenn Koordinaten gesendet wurden, erstellen wir den Punkt
        if lat is not None and lng is not None:
            validated_data['location'] = Point(float(lng), float(lat), srid=4326)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Auch beim Bearbeiten: Koordinaten aktualisieren
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        if lat is not None and lng is not None:
            instance.location = Point(float(lng), float(lat), srid=4326)

        return super().update(instance, validated_data)

class BookingSerializer(serializers.ModelSerializer):
    service = JobSerializer(read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'customer', 'customer_name', 'contractor', 'status', 'price', 'scheduled_date', 'created_at']
        read_only_fields = ['customer', 'contractor']
