from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel

class Goal(TimeStampedModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=120)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    target_date = models.DateField()

class GoalContribution(TimeStampedModel):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="contributions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()



