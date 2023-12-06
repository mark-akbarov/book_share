# Generated by Django 4.2.3 on 2023-12-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_user_telegram_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_user_id',
            field=models.PositiveIntegerField(max_length=32, null=True, unique=True),
        ),
    ]