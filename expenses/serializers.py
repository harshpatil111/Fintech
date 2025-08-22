from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    class Meta:
        model = Transaction
        fields = ("id","amount","category","category_name","date","notes","is_expense","created_at")

class AutoExpenseInputSerializer(serializers.Serializer):
    message = serializers.CharField()
    date = serializers.DateField(required=False, allow_null=True)
    txn_ref = serializers.CharField(required=False, allow_null=True)


class SmsIngestSerializer(serializers.Serializer):
    message = serializers.CharField()
    sender = serializers.CharField(required=False, allow_blank=True)
    received_at = serializers.DateTimeField(required=False)  # device timestamp
    txn_ref = serializers.CharField(required=False, allow_blank=True)
    date = serializers.DateField(required=False)             # explicit txn date override

