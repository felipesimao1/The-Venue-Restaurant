# Generated by Django 5.0.1 on 2024-01-28 04:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_reservations'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='reservations',
            new_name='Reservation',
        ),
    ]
