# Generated by Django 4.2.3 on 2023-11-20 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_condition_book_edition_book_language_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='quantity',
        ),
    ]
