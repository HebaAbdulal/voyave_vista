# Generated by Django 5.0.6 on 2024-07-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voyagevista', '0007_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
