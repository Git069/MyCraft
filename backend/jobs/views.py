from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import Job, Booking
from .serializers import JobSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    """
    Manages Services (the permanent listings by craftsmen).
    """
    # OPTIMIZATION: Use select_related to fetch contractor and profile in one query
    queryset = Job.objects.all().filter(status=Job.Status.OPEN).select_related('contractor__profile')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # We start with the optimized queryset defined above
        queryset = super().get_queryset()
        
        # --- GEO SEARCH LOGIC ---
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
        # Also optimize this custom action
        services = self.get_queryset().filter(contractor=request.user)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    """
    Manages individual Bookings of a Service.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optimization: Fetch related service and users to avoid N+1 in lists
        return Booking.objects.filter(
            Q(customer=self.request.user) | Q(contractor=self.request.user)
        ).select_related('service', 'customer', 'contractor')

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
