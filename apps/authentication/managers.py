from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group

class AppUserManager(BaseUserManager):
    def create_member_user(self, password=None, **extra_fields):
        member_group, _ = Group.objects.get_or_create(name="Member")
        user = self.create_user(password=password, **extra_fields)
        user.groups.add(member_group)
        return user

    def create_librarian_user(self, password=None, **extra_fields):
        librarian_group, _ = Group.objects.get_or_create(name="Librarian")
        user = self.create_user(password=password, **extra_fields)
        user.groups.add(librarian_group)
        return user

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(password=password, **extra_fields)
        user.groups.add(admin_group)

        return user
