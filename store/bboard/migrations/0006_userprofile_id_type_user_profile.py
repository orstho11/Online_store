# Generated by Django 3.1.7 on 2021-04-01 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_typeuserprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='id_type_user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bboard.typeuserprofile'),
            preserve_default=False,
        ),
    ]
