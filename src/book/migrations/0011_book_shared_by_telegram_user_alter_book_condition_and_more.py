# Generated by Django 4.2.3 on 2023-11-25 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0010_alter_book_description_alter_book_edition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='shared_by_telegram_user',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='condition',
            field=models.CharField(choices=[('New', 'New'), ('Like New', 'Like New'), ('Very Good', 'Very Good'), ('Good', 'Good'), ('Fair', 'Fair'), ('Poor', 'Poor')]),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Non fiction', 'Non Fiction')], null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('UZ', 'Uzbek'), ('RU', 'Russian'), ('EN', 'English')]),
        ),
        migrations.AlterField(
            model_name='book',
            name='shared_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Taken', 'Taken')]),
        ),
    ]