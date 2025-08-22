from django.db import models
from django.utils import timezone

class DashboardStat(models.Model):
    total_sessions = models.PositiveIntegerField(default=0)
    total_messages = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Dashboard Statistic"
        verbose_name_plural = "Dashboard Statistics"

    def __str__(self):
        return f"Stats as of {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"

