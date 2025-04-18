from django.conf import settings
from django.db import models

from core.models import BaseModel

class Class(BaseModel):
    name = models.CharField(max_length=4)

class Member(BaseModel):
    profile_picture = models.ImageField(upload_to="members/",max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13,blank=True,null=True)
    nis = models.CharField(max_length=13, unique=True, blank=True, null=True) # TODO: Find Real one

    account = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="member")
    _class = models.ForeignKey(name="class", to=Class, on_delete=models.SET_NULL, null=True)


class Librarian(BaseModel):
    nip = models.CharField(max_length=18)
    phone_number = models.CharField(max_length=13,blank=True,null=True)
    

    account = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="librarian")
