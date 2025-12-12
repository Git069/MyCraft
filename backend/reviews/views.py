from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import Review, Job
from .serializers import ReviewSerializer
from .permissions import IsAuthenticated

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] # Only allow logged-in users

    def perform_create(self, serializer):
        job = serializer.validated_data['job']
        user = self.request.user

        # --- PERMISSION LOGIC MOVED HERE ---
        # 1. Check if the job is completed
        if job.status != Job.Status.COMPLETED:
            raise PermissionDenied("You can only review completed jobs.")
            
        # 2. Check if the current user is the client of the job
        if job.client != user:
            raise PermissionDenied("Only the client of the job can leave a review.")
            
        # 3. Check if a review for this job already exists
        if Review.objects.filter(job=job).exists():
            raise PermissionDenied("A review for this job has already been submitted.")

        # If all checks pass, save the review with the correct users
        serializer.save(reviewer=user, recipient=job.contractor)
