# Generated by Django 3.1.1 on 2023-07-09 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20230709_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='lu',
            field=models.BooleanField(default=False),
        ),
    ]
