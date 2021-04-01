# Generated by Django 3.1.7 on 2021-04-01 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0009_auto_20210401_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('delivery_address', models.CharField(max_length=255)),
                ('date_of_submission', models.DateField()),
                ('id_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.status')),
                ('id_user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bboard.userprofile')),
            ],
        ),
    ]