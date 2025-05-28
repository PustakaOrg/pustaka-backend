from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models

from core.models import BaseModel


class SettingsManager(models.Manager):
    def get_instance(self):
        settings, _ = self.get_or_create()
        return settings


class Settings(BaseModel):
    max_loan_day = models.PositiveSmallIntegerField(default=7, null=False, blank=False, max_length=2)
    fine_per_lateday = models.DecimalField(
        max_digits=8, decimal_places=2, default=10_000, null=False, blank=False
    )
    fine_for_lost = models.DecimalField(
        max_digits=10, decimal_places=2, default=100_000, null=False, blank=False
    )
    objects = SettingsManager()

    def save(self, *args, **kwargs):
        # Ensure that only one instance can be saved
        if Settings.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of Settings can exist.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the instance
        raise PermissionDenied("This instance cannot be deleted.")
