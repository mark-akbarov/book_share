# Generated by Django 4.2.3 on 2023-12-04 08:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0014_alter_borrowedbook_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
