from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.catalog.models import Book
from apps.loan.filters import FineFilters, LoanFilters
from core.permissions import IsAdminOrLibrarianModify
from .models import Loan, Payment, Fine
from .serializers import (
    LoanSerializer,
    PaymentSerializer,
    FineSerializer,
    PopularBookSerializer,
)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = LoanFilters

    @action(detail=False, methods=["get"], url_path="popular")
    def popular_books(self, request):
        filtered_loans = self.filter_queryset(self.get_queryset())

        book_ids = filtered_loans.values_list("book__id", flat=True)

        books = (
            Book.objects.filter(id__in=book_ids)
            .annotate(loan_count=Count("loans"))
            .filter(loan_count__gt=0)
            .order_by("-loan_count")
        )
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = PopularBookSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = PopularBookSerializer(
            books, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def get_queryset(self):
        request = self.request
        queryset = super().get_queryset()

        if request.user.groups.filter(name__in=["Member"]).exists():
            return queryset.filter(borrower__account=request.user)

        return super().get_queryset()


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
