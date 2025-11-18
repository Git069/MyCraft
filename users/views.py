from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer # Diesen Serializer müssten Sie noch erstellen

class RegisterView(generics.GenericAPIView):
    # Dies ist nur ein Beispiel, wie eine DRF-View aussehen könnte
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Optional: Rückgabe von User-Daten oder einer Erfolgsmeldung
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User successfully registered.",
        }, )
