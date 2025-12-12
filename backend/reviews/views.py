from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Review
from jobs.models import Booking # Correct import
from .serializers import ReviewSerializer
from .permissions import IsAuthenticated

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The serializer expects a 'booking' ID, not 'job'
        booking = serializer.validated_data['booking']
        user = self.request.user

        # --- PERMISSION LOGIC ---
        # 1. Check if the booking is completed
        if booking.status != Booking.Status.COMPLETED:
            raise PermissionDenied("You can only review completed bookings.")
            
        # 2. Check if the current user is the customer of the booking
        if booking.customer != user:
            raise PermissionDenied("Only the customer of the booking can leave a review.")
            
        # 3. Check if a review for this booking already exists
        if Review.objects.filter(booking=booking).exists():
            raise PermissionDenied("A review for this booking has already been submitted.")

        # If all checks pass, save the review with the correct users
        serializer.save(reviewer=user, recipient=booking.contractor)
