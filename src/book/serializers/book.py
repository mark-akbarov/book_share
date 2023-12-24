import requests

from rest_framework import serializers

from core.settings import REQUEST_BOT_TOKEN
from book.models.book import Book, BookPhoto
from book.utils import generate_unique_code


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'description',
            'cover_photo',
            'telegram_photo_id',
            'code',
            'shared_by',
            'edition',
            'condition',
            'language',
            'status',
        ]


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'description',
            'cover_photo',
            'telegram_photo_id',
            'code',
            'shared_by',
            'edition',
            'condition',
            'language',
            'status',            
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    
    telegram_photo_id = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'genre',
            'description',
            'cover_photo',
            'code',
            'telegram_photo_id',
            'shared_by',
            'edition',
            'condition',
            'language',
            'status',
        )

    def get_telegram_photo_id(self, file_path):
        url = f'https://api.telegram.org/bot{REQUEST_BOT_TOKEN}/sendPhoto'
        files = {'photo': open(file_path, 'rb')}
        params = {'chat_id': 773424440}
        response = requests.post(url, params=params, files=files)
        if response.status_code == 200:
            file_id = response.json()['result']['photo'][-1]['file_id']
            return file_id
        else:
            return (f'Error uploading photo to Telegram: {response.status_code} - {response.text}')
    

    def create(self, validated_data):
        import os
        from core.settings import MEDIA_ROOT
        code = generate_unique_code()
        book = Book.objects.create(code=code, **validated_data)
        book.save()
        cover_photo = validated_data.pop('cover_photo')
        file_path = os.path.join(MEDIA_ROOT, cover_photo.name)
        book.telegram_photo_id = self.get_telegram_photo_id(file_path=file_path)
        book.save()
        return book


class BookPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPhoto
        fields = (
            'id',
            'book',
            'photo',
        )
