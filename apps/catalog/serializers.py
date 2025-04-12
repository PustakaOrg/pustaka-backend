from rest_framework import serializers
from .models import Author, Publisher, Category, Shelf, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["fullname"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "city"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ["code"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  
    publisher = PublisherSerializer(read_only=True)  
    category = CategorySerializer(many=True, read_only=True)  

    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        publisher_data = validated_data.pop('publisher', None)
        category_data = validated_data.pop('category', [])
        author = None
        publisher = None

        if author_data:
            author, created = Author.objects.get_or_create(**author_data)

        if publisher_data:
            publisher, created = Publisher.objects.get_or_create(**publisher_data)

        book = Book.objects.create(author=author, publisher=publisher, **validated_data)

        for category in category_data:
            category_obj, created = Category.objects.get_or_create(**category)

            book.category.add(category_obj)

        return book

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        publisher_data = validated_data.pop('publisher', None)
        category_data = validated_data.pop('category', [])

        if author_data:
            author, created = Author.objects.get_or_create(**author_data)
            instance.author = author

        if publisher_data:
            publisher, created = Publisher.objects.get_or_create(**publisher_data)
            instance.publisher = publisher

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.category.clear()  
        for category in category_data:
            category_obj, created = Category.objects.get_or_create(**category)
            instance.category.add(category_obj)

        return instance

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
        ]
