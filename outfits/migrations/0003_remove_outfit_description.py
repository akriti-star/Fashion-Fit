# Generated by Django 5.2.4 on 2025-07-18 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outfits', '0002_outfit_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfit',
            name='description',
        ),
    ]
