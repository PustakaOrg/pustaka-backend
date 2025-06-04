from rest_framework import  viewsets 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.serializers import UserSerializer
from apps.profiles.filters import BatchFilter, ClassFilter, MemberFilter
from core.permissions import IsAdmin, IsAdminOrLibrarianModify,  IsAdminOrLibrarianOrOwner

from .models import Batch, Class, Member, Librarian
from .serializers import BatchSerializer, ClassSerializer, MemberSerializer, LibrarianSerializer


class LibrarianViewSet(viewsets.ModelViewSet):
    queryset = Librarian.objects.all()
    serializer_class = LibrarianSerializer
    permission_classes = [IsAdmin]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminOrLibrarianOrOwner]
    filterset_class = MemberFilter

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = ClassFilter


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [IsAdminOrLibrarianModify]
    filterset_class = BatchFilter
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    try:
        member = user.member
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    except Member.DoesNotExist:
        pass

    try:
        librarian = user.librarian
        serializer = LibrarianSerializer(librarian)
        return Response(serializer.data)
    except Librarian.DoesNotExist:
        pass

    # Check if the user is an Admin
    if user.groups.filter(
        name="Admin"
    ).exists():  # Assuming admin users are marked as staff
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data , status=200)

    # If the user is neither a Member, Librarian, nor Admin
    return Response({"detail": "User profile not found."}, status=404)
