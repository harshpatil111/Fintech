from django.contrib import admin
from .models import Goal, GoalContribution

class GoalContributionInline(admin.TabularInline):
    model = GoalContribution
    extra = 1
    readonly_fields = ("date",)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "target_amount",
        "current_amount",
        "progress",
        "start_date",
        "target_date",
    )  # Removed "created"
    list_filter = ("target_date", "start_date", "user")
    search_fields = ("name", "user__username", "user__email")
    inlines = [GoalContributionInline]

    def progress(self, obj):
        if obj.target_amount > 0:
            return f"{(obj.current_amount / obj.target_amount) * 100:.2f}%"
        return "0%"
    progress.short_description = "Progress"

@admin.register(GoalContribution)
class GoalContributionAdmin(admin.ModelAdmin):
    list_display = ("goal", "amount", "date")  # Removed "created"
    list_filter = ("date", "goal__user")
    search_fields = ("goal__name", "goal__user__username", "goal__user__email")