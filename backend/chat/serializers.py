from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message
from jobs.serializers import JobSerializer

# A simple serializer for user details, used for nesting
class ParticipantSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'timestamp']

class ConversationListSerializer(serializers.ModelSerializer):
    """
    A serializer for the list view of conversations.
    Includes participant details and a preview of the last message.
    """
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
            return last_message.content[:50]
        return None

class ConversationDetailSerializer(ConversationListSerializer):
    """
    A more detailed serializer for a single conversation view, 
    including all messages. Inherits from the list serializer.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationListSerializer.Meta):
        # Inherit all fields from the base serializer and add 'messages'
        fields = ConversationListSerializer.Meta.fields + ['messages']
