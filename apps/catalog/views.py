from rest_framework import viewsets
from .models import Author, Publisher, Category, Shelf, Book
from .serializers import (
    AuthorSerializer,
    PublisherSerializer,
    CategorySerializer,
    ShelfSerializer,
    BookSerializer,
)
from core.permissions import IsAdminOrLibrarianModify


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrLibrarianModify]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrLibrarianModify]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrLibrarianModify]


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [IsAdminOrLibrarianModify]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarianModify]
