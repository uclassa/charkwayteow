# Generated by Django 5.0.1 on 2024-04-04 06:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='backend.family'),
        ),
    ]