from django.urls import path
from .views import CategoryInsightsView, MonthlyComparisonView, SavingsTrendView

urlpatterns = [
    path("categories", CategoryInsightsView.as_view()),
    path("monthly", MonthlyComparisonView.as_view()),
    path("savings", SavingsTrendView.as_view()),
]
