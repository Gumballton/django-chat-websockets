# Generated by Django 5.0.6 on 2024-05-24 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_roommodel_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='roommodel',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
