from django.db import models

from core.utils.base_model import BaseModel


class Genre(models.TextChoices):
    FICTION = 'Fiction'
    NON_FICTION = 'Non fiction'


class Condition(models.TextChoices):
    NEW = 'New'
    LIKE_NEW = 'Like New'
    VERY_GOOD = 'Very Good'
    GOOD = 'Good'
    FAIR = 'Fair'
    POOR = 'Poor'


class AvailabilityStatus(models.TextChoices):
    AVAILABLE = 'Available'
    TAKEN = 'Taken'


class Language(models.TextChoices):
    UZBEK = 'UZ'
    RUSSIAN = 'RU'
    ENGLISH = 'EN'


class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(choices=Genre.choices, null=True)
    description = models.TextField(null=True)
    cover_photo = models.FileField(null=True)
    telegram_photo_id = models.CharField(null=True)
    code = models.CharField(max_length=4, unique=True)
    shared_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='books', null=True)
    shared_by_telegram_user = models.CharField(max_length=255, null=True)
    edition = models.CharField(max_length=10, null=True)
    condition = models.CharField(choices=Condition.choices)
    language = models.CharField(choices=Language.choices)
    status = models.CharField(choices=AvailabilityStatus.choices)
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ('-created_at',)
        db_table = 'book'
    

class BookPhoto(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='photos')
    photo = models.FileField()
    
    def __str__(self) -> str:
        return self.name
