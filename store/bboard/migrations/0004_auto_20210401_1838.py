# Generated by Django 3.1.7 on 2021-04-01 16:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bboard', '0003_auto_20210401_1538'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='UserProfile',
        ),
    ]
