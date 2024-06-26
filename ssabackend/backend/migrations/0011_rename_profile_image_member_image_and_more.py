# Generated by Django 5.0.1 on 2024-04-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_alter_event_image_alter_event_image_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='profile_image',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='event',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='member',
            name='profile_image_url',
        ),
        migrations.AddField(
            model_name='event',
            name='image_id',
            field=models.CharField(blank=True, null=True, verbose_name='Image id (do not edit)'),
        ),
        migrations.AddField(
            model_name='member',
            name='image_id',
            field=models.CharField(blank=True, null=True, verbose_name='Profile image id (do not edit)'),
        ),
    ]
