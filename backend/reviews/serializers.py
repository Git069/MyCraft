from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'reviewer', 'recipient', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'recipient']
