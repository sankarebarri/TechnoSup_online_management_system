# Generated by Django 3.1.1 on 2023-06-24 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background_image',
            field=models.ImageField(blank=True, default='technosup_background_image.png', null=True, upload_to='background_image'),
        ),
    ]
