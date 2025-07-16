from django.db import models
from uuid import uuid4



class About(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=13)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



