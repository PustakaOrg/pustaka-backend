from rest_framework import viewsets
from .models import Author, Publisher, Category, Shelf, Book
from .serializers import (
    AuthorSerializer,
    PublisherSerializer,
    CategorySerializer,
    ShelfSerializer,
    BookSerializer,
)
from .permissions import IsAdminOrLibrarian


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrLibrarian]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrLibrarian]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrLibrarian]


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [IsAdminOrLibrarian]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarian]
