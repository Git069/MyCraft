from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'trade', 'zip_code', 'city', 
            'execution_date', 'price', 'status', 'created_at', 'updated_at', 
            'contractor', 'client', 'contractor_username'
        ]
        read_only_fields = ['contractor', 'client']

    def validate_price(self, value):
        """
        Check that the price is not negative.
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
