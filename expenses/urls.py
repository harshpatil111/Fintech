from django.urls import path
from .views import TransactionCreateView, TransactionListView, CategorySummaryView,AutoExpenseCreateView

urlpatterns = [
    path("add", TransactionCreateView.as_view()),
    path("list", TransactionListView.as_view()),
    path("category-summary", CategorySummaryView.as_view()),
    path('auto-add', AutoExpenseCreateView.as_view()),  # POST /api/expenses/auto-add
]
