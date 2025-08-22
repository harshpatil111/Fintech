from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Sum
from expenses.models import Transaction
from common.models import AiTip
from expenses.serializers import TransactionSerializer

class SummaryView(generics.GenericAPIView):
    def get(self, request):
        user = request.user
        income = Transaction.objects.filter(user=user, is_expense=False).aggregate(total=Sum("amount"))["total"] or 0
        expense = Transaction.objects.filter(user=user, is_expense=True).aggregate(total=Sum("amount"))["total"] or 0
        savings = (income or 0) - (expense or 0)
        return Response({
            "total_balance": float(savings),
            "monthly_expenses": float(expense),
            "savings_overview": float(savings),
        })

class TransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(notes__icontains=q)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category_id=category)
        return qs.order_by("-date","-id")

class AiTipsView(generics.GenericAPIView):
    def get(self, request):
        tip = AiTip.objects.order_by("?").first()
        return Response({ "tip": tip.text if tip else "Track expenses daily to build the habit." })

