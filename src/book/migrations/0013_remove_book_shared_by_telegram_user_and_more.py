# Generated by Django 4.2.3 on 2023-12-03 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_bookrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='shared_by_telegram_user',
        ),
        migrations.RemoveField(
            model_name='bookrequest',
            name='telegram_user_id',
        ),
    ]
