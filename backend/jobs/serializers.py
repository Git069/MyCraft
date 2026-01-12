from django.contrib.gis.geos import Point
from django.utils import timezone
from rest_framework import serializers

from .models import Booking, Job


class JobSerializer(serializers.ModelSerializer):
    """
    Serializer for Job model.
    Handles creation and updates including geolocation logic.
    """
    # We add two "write-only" fields that exist in input but not in DB
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('contractor', 'created_at', 'status',
                            'location')  # location is read-only, set via lat/lng

    def create(self, validated_data):
        """
        Creates a new Job instance.
        Extracts lat/lng to create a Point object for location.
        """
        # 1. Get coordinates from data (and remove them as they don't exist in Model)
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        # 2. If coordinates were sent, create the Point
        if lat is not None and lng is not None:
            validated_data['location'] = Point(float(lng), float(lat), srid=4326)

        # 3. FIX: Securely assign contractor
        # If not passed by perform_create, get it from request context
        if 'contractor' not in validated_data:
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                validated_data['contractor'] = request.user
            else:
                # Fallback / Error Handling if no user is present (should be prevented by permissions)
                raise serializers.ValidationError("Benutzer muss eingeloggt sein.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing Job instance.
        Updates location if lat/lng are provided.
        """
        # Update coordinates on edit as well
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)

        if lat is not None and lng is not None:
            instance.location = Point(float(lng), float(lat), srid=4326)

        return super().update(instance, validated_data)


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    Handles validation logic for booking creation.
    """
    # Read access: Show all job details
    service = JobSerializer(read_only=True)

    # Write access: Expect only job ID
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), source='service', write_only=True
    )

    customer_name = serializers.CharField(source='customer.username', read_only=True)
    review = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'service', 'service_id', 'customer', 'customer_name', 'contractor', 'status', 'price',
                  'scheduled_date', 'created_at', 'review']
        read_only_fields = ['customer', 'contractor', 'price', 'status', 'review']

    def get_review(self, obj):
        """
        Returns the ID of the review associated with this booking, if any.
        """
        try:
            return obj.review.id
        except Exception:
            return None

    def validate(self, data):
        """
        Validates business rules before booking.
        """
        user = self.context['request'].user
        # Get service object from validated data (resolved by service_id)
        service = data.get('service')
        scheduled_date = data.get('scheduled_date')

        # 1. Cannot book own services
        if service and service.contractor == user:
            raise serializers.ValidationError("Du kannst deine eigenen Dienstleistungen nicht buchen.")

        # 2. Date must be in the future
        if scheduled_date and scheduled_date < timezone.now().date():
            raise serializers.ValidationError({"scheduled_date": "Das Datum darf nicht in der Vergangenheit liegen."})

        # 3. Availability check
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
        Populates automatic fields upon creation.
        """
        service = validated_data['service']

        # Automatically take contractor from service
        validated_data['contractor'] = service.contractor

        # Save price as snapshot
        validated_data['price'] = service.price if service.price else 0

        return super().create(validated_data)
