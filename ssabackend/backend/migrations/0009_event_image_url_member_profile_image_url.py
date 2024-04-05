# Generated by Django 5.0.1 on 2024-04-05 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_event_image_alter_member_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='profile_image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
