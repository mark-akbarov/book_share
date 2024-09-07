# Generated by Django 4.2.3 on 2023-12-22 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0022_alter_bookrequest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_photo',
            field=models.FileField(default='../media/default.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Non-Fiction', 'Non Fiction'), ('Textbook', 'Textbook'), ('Self-Help', 'Self Help'), ('History', 'History'), ('Entrepreneurship', 'Entrepreneruship'), ('Programming', 'Programming'), ('Fiction', 'Fiction'), ('Sci-Fi', 'Sci Fi'), ('Romance', 'Romance'), ('Comics', 'Comics'), ('Fantasy', 'Fantasy'), ('Novel', 'Novel')], null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='telegram_photo_id',
            field=models.CharField(default='../media/default.jpg', null=True),
        ),
    ]