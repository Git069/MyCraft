from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import Job, Booking
from .serializers import JobSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly
from geopy.geocoders import Nominatim
from config.ai_utils import get_ai_response



class JobViewSet(viewsets.ModelViewSet):
    """
    Manages Services (the permanent listings by craftsmen).
    """
    # Basis-Queryset mit Optimierungen
    queryset = Job.objects.all().filter(status=Job.Status.OPEN).select_related('contractor__profile')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=False, methods=['get'])
    def suggest_address(self, request):
        query = request.query_params.get('q')
        if not query or len(query) < 3:
            return Response([])

        try:
            # WICHTIG: Immer einen eindeutigen User-Agent angeben
            geolocator = Nominatim(user_agent="mycraft_app_backend_search")

            # Wir holen die 'addressdetails=True', um Straße, PLZ, Stadt einzeln zu bekommen
            locations = geolocator.geocode(
                query,
                exactly_one=False,
                limit=5,
                addressdetails=True,
                language='de'  # Ergebnisse auf Deutsch bevorzugen
            )

            results = []
            if locations:
                for loc in locations:
                    # Nominatim liefert unterschiedliche Keys für Städte (city, town, village...)
                    addr = loc.raw.get('address', {})
                    city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('municipality') or ''

                    results.append({
                        'display_name': loc.address,  # Der volle lesbare String
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
        Gibt eine Liste aller belegten Tage (Datum) für den Handwerker dieses Jobs zurück.
        Startet ab 'heute'.
        """
        job = self.get_object()
        contractor = job.contractor

        # Nur zukünftige oder heutige Termine sind relevant
        today = timezone.now().date()

        # Wir suchen alle Buchungen dieses Handwerkers, die NICHT storniert oder erledigt sind
        busy_dates = Booking.objects.filter(
            contractor=contractor,
            scheduled_date__gte=today,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED]
        ).values_list('scheduled_date', flat=True)

        # Wir entfernen Duplikate (set) und sortieren die Liste
        # DRF wandelt die Datum-Objekte automatisch in Strings "YYYY-MM-DD" um
        return Response(sorted(list(set(busy_dates))))

    def get_queryset(self):
        queryset = super().get_queryset()

        # --- PARAMETER HOLEN ---
        search_term = self.request.query_params.get('search')
        trade_filter = self.request.query_params.get('trade')
        location_query = self.request.query_params.get('city')  # Frontend sendet 'city' für das Feld "Wo?"

        # --- 1. GEWERK FILTER (Dropdown) ---
        if trade_filter:
            queryset = queryset.filter(trade=trade_filter)

        # --- 2. INTELLIGENTE TEXTSUCHE (Was?) ---
        if search_term:
            # Suche in Titel und Beschreibung
            search_query = Q(title__icontains=search_term) | Q(description__icontains=search_term)

            # Prüfe auch, ob der Suchbegriff einem Gewerk-Namen entspricht (z.B. "Maler" -> PAINTER)
            matching_trades = []
            for code, label in Job.Trade.choices:
                if str(search_term).lower() in str(label).lower():
                    matching_trades.append(code)

            if matching_trades:
                search_query = search_query | Q(trade__in=matching_trades)

            queryset = queryset.filter(search_query)

        # --- 3. STANDORT FILTER TEXT (Wo?) ---
        # Sucht nach Stadtname ODER Postleitzahl
        if location_query:
            queryset = queryset.filter(
                Q(city__icontains=location_query) |
                Q(zip_code__startswith=location_query)
            )

        # --- 4. GEO-SEARCH (In meiner Nähe Button) ---
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius')

        if lat and lng and radius:
            try:
                user_location = Point(float(lng), float(lat), srid=4326)
                queryset = queryset.filter(
                    location__distance_lte=(user_location, D(km=float(radius)))
                ).annotate(
                    distance=Distance('location', user_location)
                ).order_by('distance')
            except (ValueError, TypeError):
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-jobs')
    def my_jobs(self, request):
        # WICHTIG: Wir nutzen Job.objects.filter(...) statt self.get_queryset()
        # Damit umgehen wir den Filter, der nur 'OPEN' Jobs anzeigt.
        # So siehst du auch pausierte oder versteckte Jobs.
        services = Job.objects.filter(contractor=request.user).order_by('-created_at')

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='price-advice')
    def price_advice(self, request, pk=None):
        """
        Fragt die KI nach einer Preiseinschätzung für diesen Job.
        """
        job = self.get_object()

        # Wir bauen einen Prompt mit den Daten des Jobs
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

        # KI fragen
        ai_reply = get_ai_response(prompt)
        return Response({'advice': ai_reply})


# ... (BookingViewSet bleibt unverändert)
class BookingViewSet(viewsets.ModelViewSet):
    # ... (Code wie zuvor)
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            Q(customer=self.request.user) | Q(contractor=self.request.user)
        ).select_related('service', 'customer', 'contractor')

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user,
            status=Booking.Status.CONFIRMED
        )

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = self.get_queryset().filter(customer=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        bookings = self.get_queryset().filter(contractor=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.contractor:
            return Response({'detail': 'Not authorized.'}, status=403)
        booking.status = Booking.Status.COMPLETED
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.customer and request.user != booking.contractor:
            return Response({'detail': 'Not authorized.'}, status=403)
        booking.status = Booking.Status.CANCELLED
        booking.save()
        return Response(self.get_serializer(booking).data)