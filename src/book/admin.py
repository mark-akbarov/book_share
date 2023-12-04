from django.contrib import admin

from book.models.book import Book, BookRequest
from book.models.borrow import BorrowedBook


admin.site.register(Book)
admin.site.register(BookRequest)
admin.site.register(BorrowedBook)
