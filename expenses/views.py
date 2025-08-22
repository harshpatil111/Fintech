from django.shortcuts import render
from rest_framework import generics,permissions
from rest_framework.response import Response
from django.db.models import Sum
from .models import Transaction
from .serializers import TransactionSerializer, AutoExpenseInputSerializer
from .utils import parse_upi_message_and_create_transaction

class TransactionCreateView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filterset_fields = ['category', 'is_expense']
    search_fields = ['notes']
    ordering_fields = ['date','amount']
    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from: qs = qs.filter(date__gte=date_from)
        if date_to: qs = qs.filter(date__lte=date_to)
        return qs

class CategorySummaryView(generics.GenericAPIView):
    def get(self, request):
        user = request.user
        data = (Transaction.objects
                .filter(user=user, is_expense=True)
                .values('category__name')
                .annotate(total=Sum('amount'))
                .order_by('-total'))
        return Response({'series': [{'label': d['category__name'], 'value': float(d['total'])} for d in data]})
    

class AutoExpenseCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AutoExpenseInputSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get('message')
        provided_date = serializer.validated_data.get('date', None)
        txn_ref = serializer.validated_data.get('txn_ref', None)

        tx, created, info = parse_upi_message_and_create_transaction(request.user, message, provided_date, txn_ref)
        if not created:
            return Response({'detail': 'Could not create transaction', 'reason': info}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification (Notification model in common)
        from common.models import Notification
        Notification.objects.create(
            user=request.user,
            title=f"New expense added: ₹{tx.amount}",
            body=f"{info.get('merchant')} — {info.get('category')}",
            link=f"/pages/expenses.html?txn_id={tx.id}"
        )

        return Response(TransactionSerializer(tx).data, status=status.HTTP_201_CREATED)
    


