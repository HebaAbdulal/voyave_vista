# Generated by Django 5.0.6 on 2024-07-05 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='average_rating',
        ),
    ]
