# Generated by Django 3.1.7 on 2021-04-01 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0006_userprofile_id_type_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bboard.userprofile')),
            ],
        ),
    ]