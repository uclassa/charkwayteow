# Generated by Django 5.0.1 on 2024-01-26 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_member_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='family',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='backend.family'),
        ),
    ]
