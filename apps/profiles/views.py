from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Member, Librarian
from .serializers import MemberSerializer, LibrarianSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
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
        if user.groups.filter(name="Admin").exists():  # Assuming admin users are marked as staff
            return Response({"detail": "Admin users do not have a profile."}, status=200)
        
        # If the user is neither a Member, Librarian, nor Admin
        return Response({"detail": "User profile not found."}, status=404)



    def post(self, request, *args, **kwargs):
        user = request.user
        
        try:
            member = user.member
            serializer = MemberSerializer(member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            pass
        
        try:
            librarian = user.librarian
            serializer = LibrarianSerializer(librarian, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Librarian.DoesNotExist:
            pass
        
        return Response({"detail": "User profile not found."}, status=404)
