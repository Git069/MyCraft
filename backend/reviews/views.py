from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from jobs.models import Booking
from .models import Review
from .permissions import IsAuthenticated
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing review instances.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom logic for creating a review.

        Ensures that:
        1. The booking is completed.
        2. The user is the customer of the booking.
        3. No review already exists for the booking.
        """
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
