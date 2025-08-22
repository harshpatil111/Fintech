from django.db import models
from django.contrib.auth import get_user_model

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(TimeStampedModel):
    EXPENSE = "expense"
    INCOME = "income"
    TYPE_CHOICES = [(EXPENSE, "Expense"), (INCOME, "Income")]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=EXPENSE)

    class Meta:
        unique_together = ("user", "name", "type")

class AiTip(TimeStampedModel):
    text = models.CharField(max_length=280)
    locale = models.CharField(max_length=8, default="en")


class MerchantMapping(models.Model):
    """
    Global keyword -> category mapping (used to auto classify merchant names).
    Keywords are checked case-insensitive inside merchant text.
    """
    keyword = models.CharField(max_length=128, help_text="keyword to match (e.g. 'swiggy')")
    category_name = models.CharField(max_length=64, help_text="category label (e.g. 'Food')")
    category_type = models.CharField(max_length=16, default='expense', choices=[('expense','Expense'),('income','Income')])
    priority = models.IntegerField(default=0, help_text="higher matches first")

    class Meta:
        ordering = ['-priority', 'keyword']

    def __str__(self):
        return f"{self.keyword} -> {self.category_name}"

class Notification(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=140)
    body = models.TextField()
    read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Notification({self.user}, read={self.read})"

