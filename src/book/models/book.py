from django.db import models

from core.utils.base_model import BaseModel


class Genre(models.TextChoices):
    TEXTBOOK = 'Textbook'
    SELF_HELP = 'Self-Help'
    HISTORY = 'History'
    ART = 'Art'
    ROMANCE = 'Romance'
    COMICS = 'Comics'
    FANTASY = 'Fantasy'
    NOVEL = 'Novel'
    


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


class BookRequestStatus(models.TextChoices):
    WAITING_FOR_RESPONSE = 'Waiting for response'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'


class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(choices=Genre.choices, null=True)
    description = models.TextField(null=True)
    cover_photo = models.FileField(null=True)
    telegram_photo_id = models.CharField(null=True)
    code = models.CharField(max_length=4, unique=True)
    shared_by = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='books', null=True)
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


class BookRequest(BaseModel):
    user = models.ForeignKey(
        'account.User', 
        on_delete=models.CASCADE, 
        related_name='requests', 
        )
    duration = models.PositiveIntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(BookRequestStatus.choices)
    
    def __str__(self) -> str:
        return str(self.id)
