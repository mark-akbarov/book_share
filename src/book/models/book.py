from django.db import models

from core.utils.base_model import BaseModel


class Genre(models.TextChoices):
    FICTION = 'fiction'
    NON_FICTION = 'non_fiction'


class Condition(models.TextChoices):
    NEW = 'new'
    LIKE_NEW = 'like_new'
    VERY_GOOD = 'very_good'
    GOOD = 'good'
    FAIR = 'fair'
    POOR = 'poor'


class AvailabilityStatus(models.TextChoices):
    AVAILABLE = 'available'
    TAKEN = 'taken'


class Language(models.TextChoices):
    UZBEK = 'uzbek'
    RUSSIAN = 'russian'
    ENGLISH = 'english'
    TAJIK = 'tajik'
    

class Book(BaseModel):
    title = models.CharField(max_length=255)
    genre = models.CharField(choices=Genre.choices)
    author = models.CharField(max_length=255)
    description = models.TextField()
    cover_photo = models.FileField(null=True)
    code = models.CharField(max_length=4, unique=True)
    shared_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='books')
    edition = models.CharField(max_length=10)
    condition = models.CharField(choices=Condition.choices)
    language = models.CharField(choices=Language.choices)
    status = models.CharField(choices=AvailabilityStatus.choices)
    
    
    def __str__(self) -> str:
        return f"{self.name} by {self.author}"
    
    class Meta:
        ordering = ('-created_at',)
        db_table = 'book'
    

class BookPhoto(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='photos')
    photo = models.FileField()
    
    def __str__(self) -> str:
        return self.name
