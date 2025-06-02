from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BatchViewSet, ClassViewSet, LibrarianViewSet, MemberViewSet,  profile_view

router = DefaultRouter()
router.register(r"members",MemberViewSet)
router.register(r"librarians",LibrarianViewSet)
router.register(r"classes", ClassViewSet)
router.register(r"batches", BatchViewSet)

urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("", include(router.urls))

]
