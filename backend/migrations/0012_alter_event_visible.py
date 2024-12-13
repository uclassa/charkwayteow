# Generated by Django 5.1.2 on 2024-11-28 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_event_event_image_folder_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='visible',
            field=models.BooleanField(default=False, verbose_name='Event visibility on telebot and website (if set to true, a new folder will be created on the drive for uploading event images)'),
        ),
    ]