from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend # Import filter backend

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    # Configure filtering
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'trade', 'city'] # Fields we can filter by

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        my_jobs_queryset = Job.objects.filter(contractor=request.user)
        serializer = self.get_serializer(my_jobs_queryset, many=True)
        return Response(serializer.data)
