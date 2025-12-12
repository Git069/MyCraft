from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from .models import Conversation, Message, Offer
from jobs.models import Job
from .serializers import ConversationListSerializer, ConversationDetailSerializer, MessageSerializer, OfferSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        OPTIMIZED: Use prefetch_related and select_related to avoid N+1 queries.
        """
        return self.request.user.conversations.select_related(
            'job'
        ).prefetch_related(
            'participants__profile', 
            'messages__offer'
        ).all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationListSerializer

    def create(self, request, *args, **kwargs):
        # ... (create logic remains the same)
        job_id = request.data.get('job_id')
        initial_message = request.data.get('message')
        if not job_id or not initial_message:
            return Response({'detail': 'Job ID and initial message are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found.'}, status=status.HTTP_404_NOT_FOUND)
        conversation = Conversation.objects.filter(job=job, participants=request.user).first()
        if not conversation:
            conversation = Conversation.objects.create(job=job)
            conversation.participants.add(request.user, job.contractor)
        Message.objects.create(conversation=conversation, sender=request.user, content=initial_message)
        serializer = ConversationDetailSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def post_message(self, request, pk=None):
        # ... (post_message logic remains the same)
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        content = request.data.get('content')
        if not content:
            return Response({'detail': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OfferViewSet(viewsets.ViewSet):
    # ... (OfferViewSet logic remains the same)
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        conversation_id = request.data.get('conversation_id')
        price = request.data.get('price')
        description = request.data.get('description')
        user = request.user
        if not user.profile.is_craftsman:
            raise PermissionDenied("Only craftsmen can create offers.")
        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=user)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found or you are not a participant.'}, status=status.HTTP_404_NOT_FOUND)
        offer = Offer.objects.create(conversation=conversation, creator=user, price=price, description=description)
        message = Message.objects.create(conversation=conversation, sender=user, offer=offer)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        user = request.user
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user == offer.creator:
            raise PermissionDenied("You cannot accept your own offer.")
        if user not in offer.conversation.participants.all():
             raise PermissionDenied("You are not a participant in this conversation.")
        offer.status = 'ACCEPTED'
        offer.save()
        job = offer.conversation.job
        job.status = 'BOOKED'
        job.client = user
        job.price = offer.price
        job.save()
        return Response(OfferSerializer(offer).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        user = request.user
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Offer not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user == offer.creator:
            raise PermissionDenied("You cannot reject your own offer.")
        if user not in offer.conversation.participants.all():
             raise PermissionDenied("You are not a participant in this conversation.")
        offer.status = 'REJECTED'
        offer.save()
        return Response(OfferSerializer(offer).data, status=status.HTTP_200_OK)
