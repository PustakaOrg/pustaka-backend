from rest_framework import serializers
from .models import Member, Librarian

class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(max_length=100)

    class Meta:
        model = Member
        fields = "__all__"

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = "__all__"
