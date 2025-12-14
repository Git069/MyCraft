from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.db.models import Avg
from .models import Profile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'username', 'email', 'password')

class CraftsmanProfileSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Profile
        fields = ('profile_picture',)

class PublicReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    reviewer_avatar = serializers.ImageField(source='reviewer.profile.profile_picture', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

class UserSerializer(BaseUserSerializer):
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
        fields = ('id', 'username', 'email', 'is_craftsman', 'company_name', 'profile_picture', 'average_rating', 'review_count', 'bio', 'city', 'reviews', 'date_joined')

    def get_average_rating(self, obj):
        return obj.received_reviews.aggregate(Avg('rating'))['rating__avg']

    def get_review_count(self, obj):
        return obj.received_reviews.count()
    
    def get_reviews(self, obj):
        reviews = obj.received_reviews.all().order_by('-created_at')[:10]
        return PublicReviewSerializer(reviews, many=True, context=self.context).data

class PublicUserSerializer(UserSerializer):
    # This serializer now just inherits from the main UserSerializer
    # as it contains all necessary public fields.
    class Meta(UserSerializer.Meta):
        pass
