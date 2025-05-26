from rest_framework import viewsets

from apps.loan.filters import FineFilters, LoanFilters
from core.permissions import IsAdminOrLibrarianModify
from .models import Loan, Payment, Fine
from .serializers import LoanSerializer, PaymentSerializer, FineSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = LoanFilters

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrLibrarianModify]

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = FineFilters

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()

        if request.user.groups.filter(name__in=["Member"]).exists():
            return queryset.filter(loan__borrower__account=request.user)
    
        return super().get_queryset()
