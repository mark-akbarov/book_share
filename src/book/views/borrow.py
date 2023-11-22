from rest_framework.viewsets import ModelViewSet

from book.models.borrow import BorrowedBook
from book.serializers.borrow import BorrowedBookSerializer


class BorrowedBookViewSet(ModelViewSet):
    queryset = BorrowedBook.objects.all()
    serializer_class = BorrowedBookSerializer