import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=255, default=uuid.uuid4, unique=True, null=True)
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    telegram_username = models.CharField(max_length=255)
    telegram_chat_id = models.CharField(max_length=15, null=True, unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telegram_username']
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"
