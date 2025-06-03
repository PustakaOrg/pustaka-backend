from rest_framework import serializers

from apps.printing.methods import generate_book_sticker_zip, generate_member_card_zip
from .models import Print
from apps.profiles.models import Member
from apps.catalog.models import Book


class PrintFilterSerializer(serializers.Serializer):
    class_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
    batch_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
    member_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
    book_ids = serializers.ListField(child=serializers.UUIDField(), required=False)
    shelf_ids = serializers.ListField(child=serializers.UUIDField(), required=False)


class PrintSerializer(serializers.ModelSerializer):
    filter = PrintFilterSerializer(write_only=True, required=False)

    class Meta:
        model = Print
        fields = ["id", "type", "file", "file_name", "filter"]
        read_only_fields = ["file"]

    def create(self, validated_data):
        file_name = validated_data["file_name"]
        print_type = validated_data["type"]
        filter_data = self.initial_data.get("filter", {})

        if print_type == "member-card":
            members = Member.objects.all()
            if "batch_ids" in filter_data:
                members = members.filter(batch__id__in=filter_data["batch_ids"])
            if "class_ids" in filter_data:
                members = members.filter(_class__id__in=filter_data["class_ids"])
            if "member_ids" in filter_data:
                members = members.filter(id__in=filter_data["member_ids"])
            file = generate_member_card_zip(members)

        elif print_type == "book-sticker":
            books = Book.objects.all()
            if "shelf_ids" in filter_data:
                books = books.filter(shelf__in=filter_data["shelf_ids"])
            if "book_ids" in filter_data:
                books = books.filter(id__in=filter_data["book_ids"])
            file = generate_book_sticker_zip(books)
        else:
            raise serializers.ValidationError("Invalid print type.")

        return Print.objects.create(
            type=print_type,
            file_name=file_name,
            file=file,
        )
