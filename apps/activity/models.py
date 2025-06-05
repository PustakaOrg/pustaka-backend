from django.db import models

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("reserved", "Book Reserved"),
        ("payment_done", "Payment Completed"),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
