# Generated by Django 5.0.7 on 2024-10-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_family_points_adjustment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
