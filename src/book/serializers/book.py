from rest_framework import serializers

from book.models.book import Book, BookPhoto
from book.utils import generate_unique_code


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
             'id',
            'name',
            'genre',
            'author',
            'description',
            'cover_photo',
            'quantity',
            'code',
            'edition',
            'condition',
            'shared_by',
            'status',
            'language',
        ]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'genre',
            'author',
            'description',
            'cover_photo',
            'code',
            'edition',
            'condition',
            'shared_by',
            'status',
            'language',
            
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'genre',
            'author',
            'description',
            'cover_photo',
            'edition',
            'condition',
            # 'shared_by',
            'status',
            'language',
        )

    def create(self, validated_data):
        code = validated_data.pop('code')
        code = generate_unique_code()
        book = Book.objects.create(code=code, **validated_data)
        return book


class BookPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPhoto
        fields = (
            'id',
            'book',
            'photo',
        )
