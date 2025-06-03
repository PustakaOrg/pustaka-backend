from django.db import models
from core.models import BaseModel

class Print(BaseModel):
    TYPE_CHOICES = [
        ('member-card', 'Member Card'),
        ('book-sticker', 'Book Sticker'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='prints/')
    file_name = models.CharField(max_length=255)
