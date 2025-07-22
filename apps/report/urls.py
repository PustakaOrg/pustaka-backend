from django.urls import path
from .views import GenerateReportPDFView 

urlpatterns = [
    path('reports/', GenerateReportPDFView.as_view(), name='generate-report'),
]
