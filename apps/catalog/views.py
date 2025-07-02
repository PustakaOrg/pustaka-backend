from rest_framework import viewsets, filters, response, status
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from rest_framework.decorators import action
from django.db import transaction

from apps.catalog.filters import AuthorFilter, BookFilter, CategoryFilter, PublisherFilter, ShelfFilter
from .models import Author, Publisher, Category, Shelf, Book
from .serializers import (
    AuthorSerializer,
    PublisherSerializer,
    CategorySerializer,
    ShelfSerializer,
    BookSerializer,
)
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from core.permissions import IsAdminOrLibrarianModify
from django.db.models import Q


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = AuthorFilter

    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        authors = Author.objects.all()
        serialized = AuthorSerializer(authors, many=True)

        return response.Response(serialized.data)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = PublisherFilter

    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        publishers = Publisher.objects.all()
        serialized = PublisherSerializer(publishers, many=True)

        return response.Response(serialized.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = CategoryFilter

    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)

        return response.Response(serialized.data)


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = ShelfFilter

    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        shelves = Shelf.objects.all()
        serialized = ShelfSerializer(shelves, many=True)

        return response.Response(serialized.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = BookFilter

    @action(detail=False, methods=["post"], url_path="import")
    def import_books(self, request):
        if "file" not in request.FILES:
            return response.Response(
                {"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES["file"]

        if not csv_file.name.endswith(".csv"):
            return response.Response(
                {"detail": "File is not a CSV."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_csv(csv_file,dtype=str)

            created_count = 0
            skipped_count = 0
            error_rows = []

            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        isbn = str(row["ISBN"]).strip()

                        if Book.objects.filter(isbn=isbn).exists():
                            skipped_count += 1
                            continue

                        author, _ = Author.objects.get_or_create(
                            fullname=row["Pengarang"].strip()
                        )
                        publisher, _ = Publisher.objects.get_or_create(
                            name=row["Penerbit"].strip()
                        )
                        category, _ = Category.objects.get_or_create(
                            name=row["Kategori"].strip()
                        )
                        shelf, _ = Shelf.objects.get_or_create(code=row["Rak"].strip())

                        book = Book.objects.create(
                            isbn=isbn,
                            title=row["Judul"].strip(),
                            publish_year=int(row["Tahun Terbit"]) if not pd.isna(row["Tahun Terbit"]) else 0,
                            stock=int(row["Jumlah"]),
                            available_stock=int(row["Jumlah"]),
                            author=author,
                            publisher=publisher,
                            shelf=shelf,
                            pages=int(row["Halaman"]) if not pd.isna(row["Halaman"]) else 0
                        )

                        book.category.add(category)
                        created_count += 1

                    except Exception as e:
                        error_rows.append({"row_index": index, "error": str(e)})
                        skipped_count += 1

            return response.Response(
                {
                    "detail": "Import completed.",
                    "created": created_count,
                    "skipped": skipped_count,
                    "errors": error_rows,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return response.Response(
                {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
