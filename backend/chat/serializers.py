from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message, Offer
from jobs.serializers import JobSerializer

class ParticipantSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'price', 'description', 'status', 'creator']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    offer = OfferSerializer(read_only=True) # Nest the offer details

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'content', 'timestamp', 'offer']

class ConversationListSerializer(serializers.ModelSerializer):
    participants_details = ParticipantSerializer(source='participants', many=True, read_only=True)
    job_details = JobSerializer(source='job', read_only=True)
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'job_details', 'participants_details', 'last_message_preview', 'updated_at']
    
    def get_last_message_preview(self, obj):
        last_message = obj.messages.last()
        if last_message:
            if last_message.offer:
                return f"Angebot: {last_message.offer.price} €"
            return last_message.content[:50]
        return None

class ConversationDetailSerializer(ConversationListSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta(ConversationListSerializer.Meta):
        fields = ConversationListSerializer.Meta.fields + ['messages']
