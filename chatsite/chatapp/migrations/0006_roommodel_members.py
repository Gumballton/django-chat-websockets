# Generated by Django 5.0.6 on 2024-05-25 16:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_roommodel_is_closed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='roommodel',
            name='members',
            field=models.ManyToManyField(related_name='joined_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
