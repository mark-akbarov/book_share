# Generated by Django 4.2.3 on 2023-12-03 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_user_id',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_chat_id',
            field=models.CharField(max_length=32, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
