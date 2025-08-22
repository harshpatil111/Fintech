from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from insights.views import CategoryInsightsView,MonthlyComparisonView, SavingsTrendView

class GoalsInsightsView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Goals insights data"}
        return Response(data)

class GoalsMonthlyComparisonView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Goals monthly comparison data"}
        return Response(data)

class GoalsTrendView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Goals trend data"}
        return Response(data)