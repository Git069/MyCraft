from rest_framework import serializers
from django.contrib.auth.models import User

from jobs.serializers import JobSerializer
from .models import Conversation, Message, Offer


class ParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for user details within a conversation.
    Includes profile picture from the related profile.
    """
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for offers made within a conversation.
    """
    class Meta:
        model = Offer
        fields = ['id', 'price', 'description', 'status', 'creator']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual chat messages.
    Includes sender details and nested offer information if present.
    """
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'timestamp', 'offer']


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing conversations.
    Provides a preview of the last message and details about participants and the related job.
    """
    participants_details = ParticipantSerializer(source='participants', many=True, read_only=True)
    job_details = JobSerializer(source='job', read_only=True)
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'job_details', 'participants_details', 'last_message_preview', 'updated_at']

    def get_last_message_preview(self, obj):
        """
        Returns a preview of the last message in the conversation.
        If the last message is an offer, returns the price.
        """
        last_message = obj.messages.last()
        if last_message:
            if last_message.offer:
                return f"Angebot: {last_message.offer.price} €"
            return last_message.content[:50]
        return None


class ConversationDetailSerializer(ConversationListSerializer):
    """
    Serializer for detailed conversation view.
    Includes all messages in the conversation.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationListSerializer.Meta):
        fields = ConversationListSerializer.Meta.fields + ['messages']
