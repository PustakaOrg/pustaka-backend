from rest_framework import serializers
from .models import Author, Publisher, Category, Shelf, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "fullname"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "city"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ["id", "code"]


class BookSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    img = serializers.ImageField(max_length=256, allow_empty_file=True)

    def create(self, validated_data):
        category_data = validated_data.pop("category",[])
        book = Book.objects.create(**validated_data)
        book.category.set(category_data)
        return book

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category", None)
        
        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if category_data is not None:
            instance.category.set(category_data)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        single_fields = [
            ("shelf", ShelfSerializer),
            ("author", AuthorSerializer),
            ("publisher", PublisherSerializer),
        ]

        for field, serializer in single_fields:
            value = getattr(instance, field, None)
            if value is not None:
                representation[field] = serializer(value).data

        many_fields = [
            ("category", CategorySerializer),
        ]

        for field, serializer in many_fields:
            values = getattr(instance, field).all()  # returns a queryset
            representation[field] = serializer(values, many=True, context=self.context).data

        return representation

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "isbn",
            "img",
            "pages",
            "publish_year",
            "stock",
            "available_stock",
            "shelf",
            "category",
            "author",
            "publisher",

            "created_at",
            "updated_at"
        ]
