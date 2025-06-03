from rest_framework.generics import ListCreateAPIView

from apps.printing.models import Print
from apps.printing.serializers import PrintSerializer
from core.permissions import IsAdminOrLibrarianOnly

class PrintListCreateView(ListCreateAPIView):
    queryset = Print.objects.all()
    serializer_class = PrintSerializer
    permission_classes = [IsAdminOrLibrarianOnly]
