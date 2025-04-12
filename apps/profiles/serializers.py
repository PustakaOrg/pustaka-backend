from rest_framework import serializers
from .models import Member, Librarian

# TODO: implement create user when creating this

class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(max_length=100)
    profile_picture = serializers.ImageField(max_length=256, allow_empty_file=True)

    class Meta:
        model = Member
        fields = "__all__"

class LibrarianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Librarian
        fields = "__all__"
