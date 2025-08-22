from django.db import models
from django.contrib.auth import get_user_model
from common.models import Category, TimeStampedModel

class Transaction(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateField()
    notes = models.CharField(max_length=255, blank=True)
    is_expense = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-id"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category"]),
        ]

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = True  # Change to True if you want Django to manage this table




class SmsIngestLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="sms_logs")
    raw_text = models.TextField()
    sender = models.CharField(max_length=64, blank=True, null=True)
    received_at = models.DateTimeField()
    parsed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    parsed_merchant = models.CharField(max_length=128, blank=True, null=True)
    parsed_ref = models.CharField(max_length=64, blank=True, null=True)
    created_txn_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["user", "parsed_ref"])]