from django.core.exceptions import ValidationError
from django.db import models

from apps.catalog.models import Book
from apps.profiles.models import Librarian, Member
from apps.settings.models import Settings
from core.models import BaseModel


class Loan(BaseModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
        ("lost", "Lost"),
        ("done", "Done"),
    ]
    loan_date = models.DateTimeField()
    return_date = models.DateTimeField()
    borrower = models.ForeignKey(
        to=Member, on_delete=models.DO_NOTHING, related_name="loans"
    )
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="loans")
    approved_by = models.ForeignKey(
        to=Librarian,
        on_delete=models.DO_NOTHING,
        related_name="approved_loans",
        null=True,
        blank=True,
    )
    return_procced_by = models.ForeignKey(
        to=Librarian,
        on_delete=models.DO_NOTHING,
        null=True,
        default=None,
        related_name="returned_loans",
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    def clean(self):
        if self.return_date < self.loan_date:
            raise ValidationError("Return date must be after load date.")

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Loan.objects.get(pk=self.pk)
            if original.status != "lost" and self.status == "lost":
                payment = Payment()
                fine_ammount = Settings.objects.get_instance().fine_for_lost
                fine = Fine(amount=fine_ammount, loan=self, payment=payment)
                fine.save()
        super().save(*args, **kwargs)  # Call the original save method


# TODO: When updating payment status to DOne update its Loan status to Done
class Payment(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]
    accepted_by = models.ForeignKey(
        to=Librarian,
        on_delete=models.DO_NOTHING,
        related_name="payments",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")


class Fine(BaseModel):
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    loan = models.ForeignKey(to=Loan, on_delete=models.CASCADE, related_name="fines")
    payment = models.ForeignKey(
        to=Payment, on_delete=models.DO_NOTHING, related_name="fines"
    )
