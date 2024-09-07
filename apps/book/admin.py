from django.contrib import admin

from apps.book.models.book import Book, BookRequest
from apps.book.models.borrow import BorrowedBook


admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(BorrowedBook)
