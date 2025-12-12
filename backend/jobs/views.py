from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly # Import custom permission

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # Apply the new permission class
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
