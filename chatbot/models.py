from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel

class ChatSession(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="chat_sessions")
    title = models.CharField(max_length=120, default="Conversation")

class ChatMessage(TimeStampedModel):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=16, choices=[("user","User"),("ai","AI")])
    content = models.TextField()

