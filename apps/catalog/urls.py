from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    AuthorViewSet,
    PublisherViewSet,
    CategoryViewSet,
    ShelfViewSet,
    BookViewSet,
)

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"publishers", PublisherViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"shelves", ShelfViewSet)
router.register(r"books", BookViewSet)

urlpatterns = [path("", include(router.urls))]
