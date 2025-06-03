from django.urls import path
from .views import PrintListCreateView
urlpatterns = [
    path("prints/", PrintListCreateView.as_view(), name="print-list-create"),
]
