from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.catalog.models import Book
from apps.loan.models import Fine, Loan, Payment
from apps.profiles.models import Member
from apps.reservation.models import Reservation
from core.permissions import IsAdminOrLibrarianOnly


#  TODO: Try implement in RAWSQL
# TODO: filter for All Time, This Week, And This Month
# TODO: implement  permission_classes

@api_view()
@permission_classes([IsAdminOrLibrarianOnly])
def get_home_data(request):
    """
    Dashboard Home
    1. Total Books
    2. Active Loan
    3. Members
    4. Overdue Loan
    """
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_overdue_loan = Loan.objects.filter(status="active").count()
    total_pending_payments = Payment.objects.filter(status="pending").count()

    result = {
        "total_books": total_books,
        "total_members": total_members,
        "total_overdue_loan": total_overdue_loan,
        "total_pending_payments": total_pending_payments,
    }
    return Response(result)


@api_view()
@permission_classes([IsAdminOrLibrarianOnly])
def get_loan_data(request):
    """
    Dashboard Loan
    1. Total Active Loan
    2. Total Overdue Loan
    3. Total Returned Loan
    4. Total Lost Loan
    """
    total_active_loan = Loan.objects.filter(status="active").count()
    total_overdue_loan = Loan.objects.filter(status="overdue").count()
    total_returned_loan = Loan.objects.filter(status="returned").count()
    total_lost_loan = Loan.objects.filter(status="lost").count()

    result = {
        "total_active_loan": total_active_loan,
        "total_overdue_loan": total_overdue_loan,
        "total_returned_loan": total_returned_loan,
        "total_lost_loan": total_lost_loan,
    }

    return Response(result)


@api_view()
@permission_classes([IsAdminOrLibrarianOnly])
def get_reservation_data(request):
    """
    Dashboard Reservation
    1. Total Pending
    2. Total Ready
    3. Total Expired
    4. Total completed
    """
    total_pending = Reservation.objects.filter(status="pending")
    total_ready = Reservation.objects.filter(status="ready")
    total_expired = Reservation.objects.filter(status="expired")
    total_completed = Reservation.objects.filter(status="completed")

    result = {
        "total_pending": total_pending,
        "total_ready": total_ready,
        "total_expired": total_expired,
        "total_completed": total_completed,
    }

    return Response(result)


@api_view()
@permission_classes([IsAdminOrLibrarianOnly])
def get_fines_data(request):
    """
    Fines
    1. Total Pending Payment
    2. Total Fines
    """

    total_pending_payments = Fine.objects.filter(payment__status="pending").count()
    total_fines = Fine.objects.filter(status="done").aggregate(
        total_amount=Sum("amount")
    )
    total_fines_ammount = total_fines["total_amount"] or 0

    result = {
        "total_pending_payments": total_pending_payments,
        "total_fines": total_fines_ammount,
    }

    return Response(result)
