from rest_framework.viewsets import ModelViewSet

from apps.book.models.borrow import BorrowedBook
from apps.book.serializers.borrow import BorrowedBookSerializer


class BorrowedBookViewSet(ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer