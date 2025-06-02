from django.db import models

from core.models import BaseModel


class Author(BaseModel):
    fullname = models.CharField(max_length=50, unique=True)


class Publisher(BaseModel):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


class Category(BaseModel):
    name = models.CharField(max_length=20, unique=True)


class Shelf(BaseModel):
    code = models.CharField(max_length=10, unique=True)


class Book(BaseModel):
    title = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    isbn = models.CharField(
        max_length=13, null=False, blank=False, unique=True, db_index=True
    )
    img = models.ImageField(upload_to="books/" ,max_length=255, blank=True, null=True)
    pages = models.PositiveSmallIntegerField(default=0)
    publish_year = models.PositiveSmallIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=1)
    available_stock = models.PositiveSmallIntegerField(default=1)
    shelf = models.ForeignKey(to=Shelf, on_delete=models.SET_NULL, null=True, related_name="books")
    category = models.ManyToManyField(to=Category, related_name="related_books", blank=True)
    author = models.ForeignKey(to=Author, on_delete=models.SET_NULL, null=True, related_name="books")
    publisher = models.ForeignKey(to=Publisher, on_delete=models.SET_NULL, null=True, related_name="books")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.available_stock = self.stock
        super().save(*args, **kwargs)





