from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'trade', 'city']

    def perform_create(self, serializer):
        if not self.request.user.profile.is_craftsman:
            raise PermissionDenied("Only craftsmen can create jobs.")
        serializer.save(contractor=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        my_jobs_queryset = Job.objects.filter(contractor=request.user)
        serializer = self.get_serializer(my_jobs_queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_bookings(self, request):
        my_bookings_queryset = Job.objects.filter(client=request.user)
        serializer = self.get_serializer(my_bookings_queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        # ... (book logic remains the same)
        job = self.get_object()
        user = request.user
        if job.status != 'OPEN':
            return Response({'detail': 'This job is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)
        if job.contractor == user:
            return Response({'detail': 'You cannot book your own job.'}, status=status.HTTP_400_BAD_REQUEST)
        job.client = user
        job.status = 'BOOKED'
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

    # --- NEW: Status Change Actions ---
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_completed(self, request, pk=None):
        job = self.get_object()
        # Only the contractor or the client can mark as completed
        if request.user != job.contractor and request.user != job.client:
            raise PermissionDenied("You are not authorized to mark this job as completed.")
        job.status = Job.Status.COMPLETED
        job.save()
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        job = self.get_object()
        # Only the contractor (owner) can cancel an open job
        if job.status == Job.Status.OPEN and request.user == job.contractor:
            job.status = Job.Status.CANCELLED
            job.save()
            return Response(self.get_serializer(job).data)
        # The client can cancel a booked job
        elif job.status == Job.Status.BOOKED and request.user == job.client:
            job.status = Job.Status.CANCELLED
            job.save()
            return Response(self.get_serializer(job).data)
        
        raise PermissionDenied("You are not authorized to cancel this job at its current status.")
