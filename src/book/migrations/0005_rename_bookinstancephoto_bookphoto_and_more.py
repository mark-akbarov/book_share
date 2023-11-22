# Generated by Django 4.2.3 on 2023-11-19 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookInstancePhoto',
            new_name='BookPhoto',
        ),
        migrations.RemoveField(
            model_name='bookphoto',
            name='book_instance',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='book_instance',
        ),
        migrations.AddField(
            model_name='bookphoto',
            name='book',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='book.book'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='borrowedbook',
            name='book',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='borrowed', to='book.book'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
    ]
