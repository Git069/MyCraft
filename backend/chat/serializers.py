from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message
from jobs.serializers import JobSerializer # Import JobSerializer

# A simple serializer for user details in conversations
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    # Nested serializers to include details directly
    participants_details = ParticipantSerializer(source='participants', many=True, read_only=True)
    job_details = JobSerializer(source='job', read_only=True)
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 
            'job_details', 
            'participants_details', 
            'last_message_preview', 
            'updated_at'
        ]
    
    def get_last_message_preview(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return last_message.content[:50] # Return first 50 chars
        return None

class ConversationDetailSerializer(ConversationSerializer):
    """
    A more detailed serializer for a single conversation view, 
    including all messages.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']
