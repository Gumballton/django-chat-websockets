# Generated by Django 5.0.6 on 2024-05-22 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagesmodel',
            name='date_message',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
