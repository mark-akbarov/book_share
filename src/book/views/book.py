from rest_framework.viewsets import ModelViewSet

from book.models.book import Book, BookPhoto
from book.serializers.book import BookSerializer, BookPhotoSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookInstancePhotoViewSet(ModelViewSet):
    queryset = BookPhoto.objects.all()
    serializer_class = BookPhotoSerializer
