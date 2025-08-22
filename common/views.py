from django.shortcuts import render

# apps/common/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import MerchantMapping, Notification
from .serializers import MerchantMappingSerializer, NotificationSerializer

class NotificationsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationMarkReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        try:
            n = Notification.objects.get(pk=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({'detail':'not found'}, status=status.HTTP_404_NOT_FOUND)
        n.read = True
        n.save()
        return Response({'detail':'marked read'}, status=status.HTTP_200_OK)

