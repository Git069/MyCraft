from rest_framework import viewsets, permissions
from rest_framework.decorators import action  # <--- WICHTIG: Importieren
from rest_framework.response import Response  # <--- WICHTIG: Importieren
from .models import Job
from .serializers import JobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(contractor=self.request.user)

    # --- NEU HINZUFÜGEN ---

    # Diese Action erstellt automatisch die URL: /api/jobs/my_jobs/
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_jobs(self, request):
        """
        Gibt nur die Jobs zurück, die vom aktuell eingeloggten User erstellt wurden.
        """
        # 1. Wir filtern: Gib mir alle Jobs, wo 'contractor' gleich 'request.user' ist
        my_jobs_queryset = Job.objects.filter(contractor=request.user)

        # 2. Wir wandeln die Daten in JSON um
        serializer = self.get_serializer(my_jobs_queryset, many=True)

        # 3. Wir schicken die Antwort zurück
        return Response(serializer.data)