# Generated by Django 4.2.7 on 2023-11-10 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_deliverylike'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='grocery',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]
