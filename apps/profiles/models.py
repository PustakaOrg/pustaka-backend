from datetime import timedelta
from django.conf import settings
from django.db import models

from core.models import BaseModel
from django.utils import timezone

def three_years_from_now():
    return timezone.now().date() + timedelta(days=3*365)

class Class(BaseModel):
    name = models.CharField(max_length=10, unique=True)


class Batch(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Member(BaseModel):
    profile_picture = models.ImageField(upload_to="members/",max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13,blank=True,null=True)
    nis = models.CharField(max_length=13, unique=True, blank=True, null=True) 
    account = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="member")
    _class = models.ForeignKey(to=Class, on_delete=models.SET_NULL, null=True)
    batch = models.ForeignKey(to=Batch, on_delete=models.SET_NULL, null=True, blank=True)
    expires_date = models.DateField(default=three_years_from_now)

    def delete(self, *args, **kwargs):
        user = self.account
        super().delete(*args, **kwargs)  
        if user:
            user.delete()                


class Librarian(BaseModel):
    nip = models.CharField(max_length=18,unique=True)
    phone_number = models.CharField(max_length=13,blank=True,null=True)
    account = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="librarian")


    def delete(self, *args, **kwargs):
        user = self.account
        super().delete(*args, **kwargs)  
        if user:
            user.delete()               
