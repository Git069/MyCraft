from django.contrib.auth.models import User
from django.db import models

from jobs.models import Job


class Conversation(models.Model):
    """
    Represents a chat conversation between users regarding a specific job.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='conversations')
    participants = models.ManyToManyField(User, related_name='conversations')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation about '{self.job.title}'"


class Offer(models.Model):
    """
    Represents a price offer made within a conversation.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='offers')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer {self.id} - {self.price} ({self.status})"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    Can optionally be linked to an Offer.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')

    content = models.TextField(blank=True, null=True)  # Content can be empty if it's just an offer container
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, null=True, blank=True, related_name='message')

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
