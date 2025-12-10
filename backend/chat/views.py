from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from jobs.models import Job
from .serializers import ConversationSerializer, ConversationDetailSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        return self.request.user.conversations.prefetch_related('messages', 'participants').all()

    def get_serializer_class(self):
        """
        Return different serializers for list and detail views.
        """
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
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
        
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=initial_message
        )

        serializer = ConversationDetailSerializer(conversation) # Return full detail on creation
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def post_message(self, request, pk=None):
        conversation = self.get_object()
        content = request.data.get('content')

        if not content:
            return Response({'detail': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
