# Generated by Django 5.1.6 on 2025-03-05 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='book_id',
            new_name='isbn',
        ),
    ]
