from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, User

from apps.profiles.models import Librarian, Member

class AppUserManager(BaseUserManager):
    def create_member_user(self, user:User, member: Member):
        student_group, _ = Group.objects.get_or_create(name="Student")
        user.member =  member
        user.groups.add(student_group)
        user.save()

        return user

    def create_admin_user(self, user: User):
        admin_group , _ = Group.objects.get_or_create(name="Admin")
        user.groups.add(admin_group)
        user.save()
        return user

    def create_librarian_user(self, user:User, librarian: Librarian):
        librarian_group , _ = Group.objects.get_or_create(name="Librarian")
        user.groups.add(librarian_group)
        user.save()
        return user

    def create_user(self, password=None, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(password=password, **extra_fields)
