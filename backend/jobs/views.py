from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from geopy.geocoders import Nominatim

from config.ai_utils import get_ai_response
from .models import Job, Booking
from .permissions import IsOwnerOrReadOnly
from .serializers import JobSerializer, BookingSerializer


class JobPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class JobViewSet(viewsets.ModelViewSet):
    """
    Manages Services (the permanent listings by craftsmen).
    """
    # Base queryset with optimizations
    queryset = Job.objects.all().filter(status=Job.Status.OPEN).select_related('contractor__profile')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = JobPagination

    def get_queryset(self):
        """
        Custom queryset filtering based on search parameters, trade, and location.
        """
        queryset = super().get_queryset()

        # --- FETCH PARAMETERS ---
        search_term = self.request.query_params.get('search')
        trade_filter = self.request.query_params.get('trade')
        location_query = self.request.query_params.get('city')
        radius = self.request.query_params.get('radius')
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        # --- 1. TRADE FILTER ---
        if trade_filter:
            queryset = queryset.filter(trade=trade_filter)

        # --- 2. TEXT SEARCH (What?) ---
        if search_term:
            search_query = Q(title__icontains=search_term) | Q(description__icontains=search_term)
            # Also search for matching trade (e.g., "Painter" in text -> Trade PAINTER)
            matching_trades = [code for code, label in Job.Trade.choices if
                               str(search_term).lower() in str(label).lower()]
            if matching_trades:
                search_query = search_query | Q(trade__in=matching_trades)
            queryset = queryset.filter(search_query)

        # --- 3. GEO & RADIUS LOGIC ---

        search_point = None
        used_radius = False  # IMPORTANT VARIABLE

        # Case A: GPS Coordinates
        if lat and lng:
            try:
                search_point = Point(float(lng), float(lat), srid=4326)
            except (ValueError, TypeError):
                pass

        # Case B: City name + Radius (Geocoding)
        elif location_query and radius:
            try:
                geolocator = Nominatim(user_agent="mycraft_backend_prod")
                # We only search in Germany to avoid "Cologne, USA"
                loc = geolocator.geocode(location_query, country_codes='de')
                if loc:
                    search_point = Point(loc.longitude, loc.latitude, srid=4326)
            except Exception as e:
                print(f"Geocoding Error: {e}")

        # --- APPLY FILTERS ---

        if search_point and radius:
            try:
                # IMPORTANT: Apply radius
                radius_km = float(radius)
                queryset = queryset.filter(
                    location__distance_lte=(search_point, D(km=radius_km))
                ).annotate(
                    distance=Distance('location', search_point)
                ).order_by('distance')

                # We note: We have filtered geographically!
                used_radius = True
            except ValueError:
                pass

        # --- 4. LOCATION TEXT FILTER (The critical part!) ---

        # We filter by city name ONLY IF we haven't already successfully filtered by radius.
        if location_query and not used_radius:
            queryset = queryset.filter(
                Q(city__icontains=location_query) |
                Q(zip_code__startswith=location_query)
            )

        return queryset

    @action(detail=False, methods=['get'])
    def suggest_address(self, request):
        """
        Suggests addresses based on a query string using Nominatim.
        """
        query = request.query_params.get('q')
        if not query or len(query) < 3:
            return Response([])

        try:
            # IMPORTANT: Always specify a unique User-Agent
            geolocator = Nominatim(user_agent="mycraft_app_backend_search")

            # We fetch 'addressdetails=True' to get street, zip code, city individually
            locations = geolocator.geocode(
                query,
                exactly_one=False,
                limit=5,
                addressdetails=True,
                language='de'  # Prefer results in German
            )

            results = []
            if locations:
                for loc in locations:
                    # Nominatim returns different keys for cities (city, town, village...)
                    addr = loc.raw.get('address', {})
                    city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('municipality') or ''

                    results.append({
                        'display_name': loc.address,  # The full readable string
                        'road': addr.get('road', ''),
                        'house_number': addr.get('house_number', ''),
                        'zip_code': addr.get('postcode', ''),
                        'city': city,
                        'lat': loc.latitude,
                        'lng': loc.longitude
                    })

            return Response(results)

        except Exception as e:
            print(f"Geocoding Error: {e}")
            return Response({'error': str(e)}, status=500)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """
        Returns a list of all booked days (dates) for the contractor of this job.
        Starts from 'today'.
        """
        job = self.get_object()
        contractor = job.contractor

        # Only future or today's appointments are relevant
        today = timezone.now().date()

        # We search for all bookings of this contractor that are NOT cancelled or completed
        busy_dates = Booking.objects.filter(
            contractor=contractor,
            scheduled_date__gte=today,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
        ).values_list('scheduled_date', flat=True)

        # We remove duplicates (set) and sort the list
        # DRF automatically converts date objects to strings "YYYY-MM-DD"
        return Response(sorted(list(set(busy_dates))))

    @action(detail=False, methods=['get'], url_path='my-jobs')
    def my_jobs(self, request):
        """
        Returns jobs belonging to the authenticated contractor.
        """
        # IMPORTANT: We use Job.objects.filter(...) instead of self.get_queryset()
        # This bypasses the filter that only shows 'OPEN' jobs.
        # This allows seeing paused or hidden jobs.
        services = Job.objects.filter(contractor=request.user).order_by('-created_at')

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='price-advice')
    def price_advice(self, request, pk=None):
        """
        Asks the AI for a price estimate for this job.
        """
        job = self.get_object()

        # We build a prompt with the job data
        prompt = (
            f"Du bist ein Experte für Handwerkerpreise in Deutschland. "
            f"Ein Kunde fragt nach einer Preiseinschätzung. "
            f"Details: "
            f"Gewerk: {job.get_trade_display()}. "
            f"Ort: {job.zip_code} {job.city}. "
            f"Beschreibung: {job.description}. "
            f"Bitte gib eine realistische Preisspanne an und erkläre kurz, wovon der Preis abhängt. "
            f"Antworte direkt an den Kunden (per 'Du'). Halte es kurz (max 3 Sätze)."
        )

        # Ask AI
        ai_reply = get_ai_response(prompt)
        return Response({'advice': ai_reply})


class BookingViewSet(viewsets.ModelViewSet):
    """
    Manages Bookings between customers and contractors.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns bookings where the user is either customer or contractor.
        """
        return Booking.objects.filter(
            Q(customer=self.request.user) | Q(contractor=self.request.user)
        ).select_related('service', 'customer', 'contractor')

    def perform_create(self, serializer):
        """
        Sets the customer to the current user and status to CONFIRMED upon creation.
        """
        serializer.save(
            customer=self.request.user,
            status=Booking.Status.CONFIRMED
        )

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """
        Returns bookings where the user is the customer.
        """
        bookings = self.get_queryset().filter(customer=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Returns bookings where the user is the contractor.
        """
        bookings = self.get_queryset().filter(contractor=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """
        Marks a booking as completed. Only allowed for the contractor.
        """
        booking = self.get_object()
        if request.user != booking.contractor:
            return Response({'detail': 'Not authorized.'}, status=403)
        booking.status = Booking.Status.COMPLETED
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        user = request.user

        # Check authorization
        if user != booking.contractor and user != booking.customer:
            return Response(
                {'detail': 'Du bist nicht berechtigt, diese Buchung zu stornieren.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Logic for CUSTOMERS: 7-day rule
        if user == booking.customer:
            if booking.scheduled_date:
                today = timezone.now().date()
                days_until_job = (booking.scheduled_date - today).days

                if days_until_job < 7:
                    return Response(
                        {'detail': 'Stornierung für Kunden nur bis zu 7 Tage vor dem Termin möglich.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # Check if already cancelled
        if booking.status == Booking.Status.CANCELLED:
            return Response({'detail': 'Buchung ist bereits storniert.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = Booking.Status.CANCELLED
        booking.save()

        return Response(self.get_serializer(booking).data)
