from rest_framework import serializers
from .models import Member, Librarian

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = "__all__"
