"""
Views for the Users application.

This module defines the API views for the Users application, handling user
registration, profile management, and craftsman status upgrades.
"""

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CraftsmanProfileSerializer,
    ProfilePictureSerializer,
    PublicUserSerializer,
    UserCreateSerializer,
    UserProfileUpdateSerializer,
)


# --- Authentication & User Management Views ---

class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    Allows any user to register a new account using the UserCreateSerializer.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer


class CustomUserViewSet(DjoserUserViewSet):
    """
    Custom UserViewSet that overrides Djoser's default behavior.

    This viewset handles standard user operations provided by Djoser but
    customizes the serializer used for specific actions.
    """

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.

        Overrides the default behavior to use PublicUserSerializer when
        retrieving a specific user's details (public profile).
        For all other actions (e.g., 'me', 'list'), it defaults to Djoser's configuration.

        Returns:
            Serializer class to be used.
        """
        # Use PublicUserSerializer for the public retrieve action
        if self.action == 'retrieve':
            return PublicUserSerializer
        # For all other actions (me, list, etc.), use the default from Djoser
        return super().get_serializer_class()


# --- Profile Management Views ---

class UserProfileUpdateView(generics.UpdateAPIView):
    """
    API view for updating the authenticated user's profile.

    Allows the user to update their profile details.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        """
        Retrieve the profile instance associated with the current user.

        Returns:
            Profile: The profile instance of the authenticated user.
        """
        return self.request.user.profile


class ProfilePictureUploadView(generics.UpdateAPIView):
    """
    API view for uploading a profile picture.

    Supports multipart/form-data and form-urlencoded requests to update
    the user's profile picture.
    """
    serializer_class = ProfilePictureSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        """
        Retrieve the profile instance associated with the current user.

        Returns:
            Profile: The profile instance of the authenticated user.
        """
        return self.request.user.profile


class BecomeCraftsmanView(APIView):
    """
    API view to upgrade a user to a craftsman.

    This view handles the logic for a user applying to become a craftsman.
    It updates the user's profile with craftsman details and sets the
    is_craftsman flag to True.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to become a craftsman.

        Validates the provided data against the CraftsmanProfileSerializer.
        If valid, saves the data and ensures the user is marked as a craftsman.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: HTTP response indicating success or failure.
        """
        user_profile = request.user.profile
        serializer = CraftsmanProfileSerializer(instance=user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Ensure the user is marked as a craftsman if not already
            if not user_profile.is_craftsman:
                user_profile.is_craftsman = True
                user_profile.save()

            return Response({"detail": "You are now a craftsman."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
