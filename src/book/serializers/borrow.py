from rest_framework import serializers

from book.models.borrow import BorrowedBook


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = [
            'id',
            'borrower',
            'book_instance',
            'borrow_date',
            'return_date',
            'status',
        ]
