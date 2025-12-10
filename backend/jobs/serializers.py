from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    # Add a read-only field to get the contractor's username
    contractor_username = serializers.CharField(source='contractor.username', read_only=True)

    class Meta:
        model = Job
        # Add the new field to the list of fields
        fields = [
            'id', 'title', 'description', 'trade', 'zip_code', 'city', 
            'execution_date', 'price', 'status', 'created_at', 'updated_at', 
            'contractor', 'client', 'contractor_username'
        ]
        # Make contractor and client read-only in the main serializer
        # They are set automatically in the view (perform_create) or via other actions
        read_only_fields = ['contractor', 'client']
