# Generated by Django 5.0.3 on 2024-03-14 06:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_rename_id_prrof_teacherdocument_id_proof_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherdocument',
            name='teacher',
        ),
        migrations.AddField(
            model_name='teacherdocument',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
