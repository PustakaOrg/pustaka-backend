from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LibrarianViewSet, MemberViewSet, ProfileView

router = DefaultRouter()
router.register(r"members",MemberViewSet)
router.register(r"librarians",LibrarianViewSet)

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("", include(router.urls))

]
