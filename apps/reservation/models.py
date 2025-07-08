from django.db import models

from apps.catalog.models import Book
from apps.profiles.models import Librarian, Member
from core.models import BaseModel


class Reservation(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("ready", "Ready"),
        ("canceled", "canceled"),
        ("completed", "Completed"),
        ("expired", "Expired"),
    ]

    reservation_date = models.DateField()
    pickup_date = models.DateField()
    day_to_loan = models.PositiveSmallIntegerField(default=1)
    reservant = models.ForeignKey(
        to=Member, on_delete=models.CASCADE, related_name="reservations"
    )
    book = models.ForeignKey(
        to=Book, on_delete=models.CASCADE, related_name="reservations"
    )
    accepted_by = models.ForeignKey(
        to=Librarian,
        on_delete=models.SET_NULL,
        related_name="reservations",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                previous = Reservation.objects.get(pk=self.pk)
                if previous.status in ["pending", "ready"] and self.status in ["canceled", "expired"]:
                    self.book.available_stock += 1
                    self.book.save()
            except Reservation.DoesNotExist:
                pass  # This can happen on first save()
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if self.status in ["pending", "ready"]:
            self.book.available_stock += 1
            self.book.save()
        return super().delete(*args, **kwargs)

