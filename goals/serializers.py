from rest_framework import serializers
from .models import Goal, GoalContribution

class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    class Meta:
        model = Goal
        fields = ("id","name","target_amount","current_amount","start_date","target_date","progress","created_at")
    def get_progress(self, obj):
        if obj.target_amount and obj.target_amount > 0:
            return round(float(obj.current_amount) / float(obj.target_amount) * 100, 2)
        return 0

class GoalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalContribution
        fields = ("id","goal","amount","date","created_at")
