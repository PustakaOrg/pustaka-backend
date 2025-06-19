from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.catalog.models import Book
from apps.loan.models import Fine, Loan, Payment
from apps.profiles.models import Member
from apps.reservation.models import Reservation
from core.permissions import IsAdminOrLibrarianOnly


@api_view()
@permission_classes([IsAdminOrLibrarianOnly])
def get_home_data(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    total_overdue_loan = Loan.objects.filter(status="overdue").count()
    total_pending_payments = Payment.objects.filter(status="pending").count()

    result = {
        "total_books": total_books,
        "total_members": total_members,
        "total_overdue_loan": total_overdue_loan,
        "total_pending_payments": total_pending_payments,
    }
    return Response(result)
