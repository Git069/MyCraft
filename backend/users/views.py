from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from djoser.views import UserViewSet as DjoserUserViewSet
from .serializers import UserCreateSerializer, CraftsmanProfileSerializer, ProfilePictureSerializer, PublicUserSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

class BecomeCraftsmanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_profile = request.user.profile
        serializer = CraftsmanProfileSerializer(instance=user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if not user_profile.is_craftsman:
                user_profile.is_craftsman = True
                user_profile.save()
            return Response({"detail": "You are now a craftsman."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfilePictureUploadView(generics.UpdateAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

# --- NEW: Override Djoser's UserViewSet ---
class CustomUserViewSet(DjoserUserViewSet):
    def get_serializer_class(self):
        # Use PublicUserSerializer for the public retrieve action
        if self.action == 'retrieve':
            return PublicUserSerializer
        # For all other actions (me, list, etc.), use the default from Djoser
        return super().get_serializer_class()
