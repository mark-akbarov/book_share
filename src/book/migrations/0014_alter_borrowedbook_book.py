# Generated by Django 4.2.3 on 2023-12-03 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_remove_book_shared_by_telegram_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowedbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed', to='book.book'),
        ),
    ]
