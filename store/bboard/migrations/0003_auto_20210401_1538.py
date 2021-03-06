# Generated by Django 3.1.7 on 2021-04-01 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_author_producttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id_author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bboard.author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='id_product_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bboard.producttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
