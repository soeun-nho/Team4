# Generated by Django 4.2.7 on 2023-11-09 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_create_db'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='writer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='deliverycomment',
            old_name='writer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='grocery',
            old_name='writer',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='grocerycomment',
            old_name='writer',
            new_name='user',
        ),
    ]