from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.utils import timezone  # <--- WICHTIG: Dieser Import hat gefehlt!
from .models import Job, Booking


class JobSerializer(serializers.ModelSerializer):
    # Wir fügen zwei "Schreib-Felder" hinzu, die nicht in der DB, aber im Input existieren
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('contractor', 'created_at', 'status',
                            'location')  # location ist read-only, wird via lat/lng gesetzt

    def create(self, validated_data):
        # 1. Koordinaten aus den Daten holen (und entfernen, da sie nicht im Model existieren)
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        # 2. Wenn Koordinaten gesendet wurden, erstellen wir den Punkt
        if lat is not None and lng is not None:
            validated_data['location'] = Point(float(lng), float(lat), srid=4326)

        # 3. FIX: Contractor sicher zuweisen
        # Falls er nicht durch perform_create übergeben wurde, holen wir ihn aus dem Request-Kontext
        if 'contractor' not in validated_data:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                validated_data['contractor'] = request.user
            else:
                # Fallback / Error Handling, falls kein User da ist (sollte durch Permissions nicht passieren)
                raise serializers.ValidationError("Benutzer muss eingeloggt sein.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Auch beim Bearbeiten: Koordinaten aktualisieren
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        if lat is not None and lng is not None:
            instance.location = Point(float(lng), float(lat), srid=4326)

        return super().update(instance, validated_data)


class BookingSerializer(serializers.ModelSerializer):
    # Lesender Zugriff: Wir zeigen alle Details des Jobs
    service = JobSerializer(read_only=True)

    # Schreibender Zugriff: Wir erwarten nur die ID des Jobs
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='service', write_only=True
    )

    customer_name = serializers.CharField(source='customer.username', read_only=True)
    review = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'service', 'service_id', 'customer', 'customer_name', 'contractor', 'status', 'price', 'scheduled_date', 'created_at', 'review']
        read_only_fields = ['customer', 'contractor', 'price', 'status', 'review']

    def get_review(self, obj):
        try:
            return obj.review.id
        except Exception:
            return None

    def validate(self, data):
        """
        Prüft Geschäftsregeln vor der Buchung.
        """
        user = self.context['request'].user
        # Wir holen das Service-Objekt aus den validierten Daten (wurde durch service_id aufgelöst)
        service = data.get('service')
        scheduled_date = data.get('scheduled_date')

        # 1. Eigene Services darf man nicht buchen
        if service and service.contractor == user:
            raise serializers.ValidationError("Du kannst deine eigenen Dienstleistungen nicht buchen.")

        # 2. Datum muss in der Zukunft liegen
        if scheduled_date and scheduled_date < timezone.now().date():
            raise serializers.ValidationError({"scheduled_date": "Das Datum darf nicht in der Vergangenheit liegen."})

        # 3. Verfügbarkeits-Check
        if service and scheduled_date:
            is_busy = Booking.objects.filter(
                contractor=service.contractor,
                scheduled_date=scheduled_date,
                status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
            ).exists()

            if is_busy:
                raise serializers.ValidationError(
                    {"scheduled_date": "Der Handwerker ist an diesem Datum bereits ausgebucht."}
                )

        return data

    def create(self, validated_data):
        """
        Füllt automatische Felder beim Erstellen.
        """
        service = validated_data['service']

        # Automatisch den Handwerker aus dem Service übernehmen
        validated_data['contractor'] = service.contractor

        # Preis als Snapshot speichern
        validated_data['price'] = service.price if service.price else 0

        return super().create(validated_data)