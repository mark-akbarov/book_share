from rest_framework.viewsets import ModelViewSet

from book.models.book import Book, BookPhoto
from book.serializers.book import BookSerializer, BookPhotoSerializer, BookCreateSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    # serializer_class = BookSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'list':
            return BookSerializer


class BookInstancePhotoViewSet(ModelViewSet):
    queryset = BookPhoto.objects.all()
    serializer_class = BookPhotoSerializer
