from rest_framework import viewsets, generics
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

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get("q", None)
        author_fullnames = self.request.query_params.getlist("author")
        category_names = self.request.query_params.getlist("category")
        publisher_names = self.request.query_params.getlist("publisher")
        published_year = self.request.query_params.get("publish_year", None)
        available = self.request.query_params.get("available", None)

        filters = Q()

        if query:
            # Use Postgres FTS for improving performance
            search_vector = SearchVector("title", "author__fullname", "isbn")
            search_query = SearchQuery(query)
            filters |= Q(rank__gt=0)  # This will be applied later

            # Annotate the queryset with rank
            queryset = Book.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(filters)  

        if author_fullnames:
            filters &= Q(
                author__fullname__in=author_fullnames
            )  
        if category_names:
            filters &= Q(category__name__in=category_names)  
        if publisher_names:
            filters &= Q(publisher__name__in=publisher_names)  
        if published_year:
            filters &= Q(publish_year=published_year)  
        if available:
            filters &= Q(available_stock__gt=0)


        if filters:
            queryset = queryset.filter(filters)
        return queryset

