from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

class CategoryInsightsView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Category insights data"}
        return Response(data)

class MonthlyComparisonView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Monthly comparison data"}
        return Response(data)
    
class SavingsTrendView(APIView):
    def get(self, request):
        # Replace with your logic
        data = {"message": "Savings trend data"}
        return Response(data)