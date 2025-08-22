from django.contrib import admin
from .models import Transaction, ExpenseCategory,SmsIngestLog

admin.site.register(Transaction)
admin.site.register(ExpenseCategory)


@admin.register(SmsIngestLog)
class SmsIngestLogAdmin(admin.ModelAdmin):
    list_display = ("user", "sender", "parsed_amount", "parsed_merchant", "parsed_ref", "created_txn_id", "created")
    search_fields = ("raw_text", "parsed_merchant", "parsed_ref", "sender", "user__username")
    list_filter = ("sender",)