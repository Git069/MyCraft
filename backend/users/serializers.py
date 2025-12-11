from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
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

class UserSerializer(BaseUserSerializer):
    is_craftsman = serializers.BooleanField(source='profile.is_craftsman', read_only=True)
    company_name = serializers.CharField(source='profile.company_name', read_only=True)
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'is_craftsman', 'company_name', 'profile_picture')
