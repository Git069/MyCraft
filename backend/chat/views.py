from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from config.ai_utils import get_ai_response
from jobs.models import Booking, Job
from .models import Conversation, Message, Offer
from .serializers import (
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageSerializer,
    OfferSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Provides endpoints for listing, retrieving, and creating conversations,
    as well as posting messages and generating AI suggestions.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns the list of conversations for the authenticated user,
        including related messages and participant profiles.
        """
        return self.request.user.conversations.prefetch_related(
            'messages', 'participants__profile'
        ).all()

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the current action.
        """
        if self.action == 'list':
            return ConversationListSerializer
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationListSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new conversation for a specific job.
        If a conversation already exists, it returns the existing one.
        """
        job_id = request.data.get('job_id')
        initial_message = request.data.get('message')

        if not job_id or not initial_message:
            return Response(
                {'detail': 'Job ID and initial message are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {'detail': 'Job not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        conversation = Conversation.objects.filter(
            job=job, participants=request.user
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(job=job)
            conversation.participants.add(request.user, job.contractor)

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=initial_message
        )

        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def post_message(self, request, pk=None):
        """
        Adds a new message to the conversation.
        """
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        content = request.data.get('content')
        if not content:
            return Response(
                {'detail': 'Message content is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='suggest-reply')
    def suggest_reply(self, request):
        """
        Generates a suggested reply using AI.
        Expected body: { 'last_message': '...' }
        """
        last_message = request.data.get('last_message', '')

        if not last_message:
            return Response({'suggestion': 'No message found to reply to.'})

        # Prompt remains in German to maintain functional behavior for German users
        prompt = (
            f"Du bist ein freundlicher, professioneller Handwerker. "
            f"Ein Kunde hat dir geschrieben: '{last_message}'. "
            f"Verfasse eine kurze, höfliche Antwort, die Interesse zeigt oder auf die Frage eingeht. "
            f"Schreibe nur den Antworttext ohne Anführungszeichen."
        )

        ai_reply = get_ai_response(prompt)
        return Response({'suggestion': ai_reply})


class OfferViewSet(viewsets.ViewSet):
    """
    ViewSet for managing offers.
    Allows craftsmen to create offers and users to accept or reject them.
    """
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """
        Creates a new offer within a conversation.
        Only users with a craftsman profile can create offers.
        """
        conversation_id = request.data.get('conversation_id')
        price = request.data.get('price')
        description = request.data.get('description')
        user = request.user

        if not user.profile.is_craftsman:
            raise PermissionDenied("Only craftsmen can create offers.")

        try:
            conversation = Conversation.objects.get(
                id=conversation_id, participants=user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'detail': 'Conversation not found or you are not a participant.'},
                status=status.HTTP_404_NOT_FOUND
            )

        offer = Offer.objects.create(
            conversation=conversation,
            creator=user,
            price=price,
            description=description
        )
        message = Message.objects.create(
            conversation=conversation,
            sender=user,
            offer=offer
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """
        Accepts an offer and creates a corresponding booking.
        """
        user = request.user
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user == offer.creator:
            raise PermissionDenied("You cannot accept your own offer.")
        if user not in offer.conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        offer.status = 'ACCEPTED'
        offer.save()

        service = offer.conversation.job
        Booking.objects.create(
            service=service,
            customer=user,
            contractor=service.contractor,
            price=offer.price,
            status=Booking.Status.CONFIRMED
        )

        return Response(OfferSerializer(offer).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Rejects an offer.
        """
        user = request.user
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response(
                {'detail': 'Offer not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user == offer.creator:
            raise PermissionDenied("You cannot reject your own offer.")
        if user not in offer.conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        offer.status = 'REJECTED'
        offer.save()
        return Response(OfferSerializer(offer).data, status=status.HTTP_200_OK)
