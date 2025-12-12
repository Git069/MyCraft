from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Job, Booking
from .serializers import JobSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    """
    Manages Services (the permanent listings by craftsmen).
    """
    queryset = Job.objects.all().filter(status=Job.Status.OPEN)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)

    @action(detail=False, methods=['get'], url_path='my-jobs')
    def my_jobs(self, request):
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
        return Booking.objects.filter(
            Q(customer=self.request.user) | Q(contractor=self.request.user)
        )

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = Booking.objects.filter(customer=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        bookings = Booking.objects.filter(contractor=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    # --- NEW: Status Change Actions for Bookings ---
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        booking = self.get_object()
        # Permission: Only the contractor of the booking can mark it as completed
        if request.user != booking.contractor:
            return Response({'detail': 'Not authorized.'}, status=403)
        
        booking.status = Booking.Status.COMPLETED
        booking.save()
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        # Permission: Either the customer or contractor can cancel
        if request.user != booking.customer and request.user != booking.contractor:
            return Response({'detail': 'Not authorized.'}, status=403)
            
        booking.status = Booking.Status.CANCELLED
        booking.save()
        return Response(self.get_serializer(booking).data)
