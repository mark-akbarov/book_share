from django.db import models

from core.utils.base_model import BaseModel


class BorrowedBookStatus(models.TextChoices):
    BORROWED = 'borrowed'
    RETURNED = 'returned'
    OVERDUE = 'overdue'


class BorrowedBook(BaseModel):
    borrower = models.OneToOneField('account.User', on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.OneToOneField('book.Book', on_delete=models.CASCADE, related_name='borrowed')
    borrow_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(BorrowedBookStatus.choices)
    
    def __str__(self) -> str:
        return f"{self.borrower} - {self.book_instance}"
