from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'trade', 'city']

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        my_jobs_queryset = Job.objects.filter(contractor=request.user)
        serializer = self.get_serializer(my_jobs_queryset, many=True)
        return Response(serializer.data)

    # --- NEW: Book Job Action ---
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def book(self, request, pk=None):
        job = self.get_object()
        user = request.user

        # --- Validation ---
        if job.status != 'OPEN':
            return Response({'detail': 'This job is no longer available.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if job.contractor == user:
            return Response({'detail': 'You cannot book your own job.'}, status=status.HTTP_400_BAD_REQUEST)

        # --- Logic ---
        job.client = user
        job.status = 'BOOKED'
        job.save()

        serializer = self.get_serializer(job)
        return Response(serializer.data)
