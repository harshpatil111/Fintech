from django.urls import path
from .views import SummaryView, TransactionsView, AiTipsView

urlpatterns = [
    path("summary", SummaryView.as_view()),
    path("transactions", TransactionsView.as_view()),
    path("ai-tips", AiTipsView.as_view()),
]
