from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import AppUserManager

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []    

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = None
    first_name = None
    last_name = None
    fullname = models.CharField(max_length=100,)
    email = models.EmailField('email address', unique=True)    
    objects = AppUserManager()    

    def __str__(self):
        return self.email
