from django.db import models

from apps.catalog.models import Book
from apps.profiles.models import Librarian, Member
from core.models import BaseModel


class Reservation(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("ready", "Ready"),
        ("completed", "Completed"),
        ("expired", "Expired"),

    ]
    reservation_date = models.DateTimeField()
    pickup_date = models.DateTimeField()
    reservant = models.ForeignKey(to=Member, on_delete=models.DO_NOTHING, related_name="reservations")
    book = models.ForeignKey(to=Book, on_delete=models.DO_NOTHING,related_name="reservations")
    accepted_by = models.ForeignKey(to=Librarian, on_delete=models.DO_NOTHING,related_name="reservations", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
