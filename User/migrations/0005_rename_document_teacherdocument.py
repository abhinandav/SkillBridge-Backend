# Generated by Django 5.0.3 on 2024-03-14 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_document'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Document',
            new_name='TeacherDocument',
        ),
    ]
