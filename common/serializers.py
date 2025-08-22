# apps/common/serializers.py
from rest_framework import serializers
from .models import MerchantMapping, Notification

class MerchantMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantMapping
        fields = ['id','keyword','category_name','category_type','priority']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','title','body','read','link','created_at']
