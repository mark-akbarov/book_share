# Generated by Django 4.2.3 on 2023-12-04 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_remove_borrowedbook_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrequest',
            name='duration',
        ),
    ]
