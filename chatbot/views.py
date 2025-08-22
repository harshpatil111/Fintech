from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import ChatSession, ChatMessage

class QueryView(generics.GenericAPIView):
    def post(self, request):
        text = request.data.get("text","")
        session_id = request.data.get("session_id")
        if session_id:
            session = ChatSession.objects.filter(id=session_id, user=request.user).first()
        else:
            session = ChatSession.objects.create(user=request.user)
        ChatMessage.objects.create(session=session, role="user", content=text)
        # simple stub reply:
        reply = f"You said: {text}. (Insights & charts will appear here.)"
        ChatMessage.objects.create(session=session, role="ai", content=reply)
        return Response({"session_id": session.id, "reply": reply})

class VoiceView(generics.GenericAPIView):
    def post(self, request):
        return Response({"detail": "Voice processing pending integration."})

