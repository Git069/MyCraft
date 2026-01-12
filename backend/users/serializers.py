"""Serializers for the Users application.

This module contains serializers for user registration, profile management,
and public user representation, including craftsman details and reviews.
"""

from django.db.models import Avg
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import Profile


# --- User Registration Serializers ---

class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer for user registration.

    Inherits from Djoser's UserCreateSerializer to handle user creation
    with standard fields.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'username', 'email', 'password')


# --- Profile Management Serializers ---

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile details.

    Allows updating bio, city, company name, address, and zip code.
    """
    class Meta:
        model = Profile
        fields = ('bio', 'city', 'company_name', 'street_address', 'zip_code')
        # All fields are optional here (required=False is default in ModelSerializer
        # for these fields, unless the model enforces it, but in the model they are blank=True)


class CraftsmanProfileSerializer(serializers.ModelSerializer):
    """Serializer for craftsman profile details.

    Used when a user applies to become a craftsman. Enforces required fields
    for business information.
    """
    class Meta:
        model = Profile
        fields = ('company_name', 'street_address', 'zip_code', 'city', 'bio')
        extra_kwargs = {
            'company_name': {'required': True},
            'street_address': {'required': True},
            'zip_code': {'required': True},
            'city': {'required': True},
        }


class ProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer for updating the profile picture."""
    class Meta:
        model = Profile
        fields = ('profile_picture',)


# --- Public Representation Serializers ---

class PublicReviewSerializer(serializers.Serializer):
    """Serializer for representing a review publicly.

    Read-only serializer to display review details including the reviewer's
    name, avatar, and the associated job title.
    """
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    reviewer_avatar = serializers.ImageField(source='reviewer.profile.profile_picture', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)


class UserSerializer(BaseUserSerializer):
    """Serializer for detailed user representation.

    Includes standard user fields plus profile-specific fields like
    craftsman status, company details, average rating, and recent reviews.
    """
    is_craftsman = serializers.BooleanField(source='profile.is_craftsman', read_only=True)
    company_name = serializers.CharField(source='profile.company_name', read_only=True)
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    bio = serializers.CharField(source='profile.bio', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    reviews = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = (
            'id', 'username', 'email', 'is_craftsman', 'company_name',
            'profile_picture', 'average_rating', 'review_count', 'bio',
            'city', 'reviews', 'date_joined'
        )

    def get_average_rating(self, obj):
        """Calculate the average rating from received reviews.

        Args:
            obj: The user instance.

        Returns:
            float: The average rating or None.
        """
        return obj.received_reviews.aggregate(Avg('rating'))['rating__avg']

    def get_review_count(self, obj):
        """Count the total number of received reviews.

        Args:
            obj: The user instance.

        Returns:
            int: The count of reviews.
        """
        return obj.received_reviews.count()

    def get_reviews(self, obj):
        """Retrieve the 10 most recent reviews for the user.

        Args:
            obj: The user instance.

        Returns:
            list: A list of serialized review data.
        """
        reviews = obj.received_reviews.all().order_by('-created_at')[:10]
        return PublicReviewSerializer(reviews, many=True, context=self.context).data


class PublicUserSerializer(UserSerializer):
    """Serializer for public user profiles.

    Inherits from UserSerializer to expose the same fields for public viewing.
    """
    # This serializer now just inherits from the main UserSerializer
    # as it contains all necessary public fields.
    class Meta(UserSerializer.Meta):
        pass
