from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models

from core.models import BaseModel


class SettingsManager(models.Manager):
    def get_instance(self):
        # Get the single instance of Settings
        settings, _ = self.get_or_create()
        return settings


class Settings(BaseModel):
    max_loan_day = models.PositiveSmallIntegerField(max_length=2)
    fine_per_lateday = models.FloatField(max_length=4)
    fine_for_lost = models.FloatField(max_length=4)
    objects = SettingsManager()

    def save(self, *args, **kwargs):
        # Ensure that only one instance can be saved
        if Settings.objects.exists() and not self.pk:
            raise ValidationError("Only one instance of Settings can exist.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the instance
        raise PermissionDenied("This instance cannot be deleted.")
