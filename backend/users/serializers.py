from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import Profile

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'username', 'email', 'password')

class UserSerializer(BaseUserSerializer):
    is_craftsman = serializers.BooleanField(source='profile.is_craftsman', read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'username', 'email', 'is_craftsman')
