# Generated by Django 5.0.7 on 2024-10-20 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_rename_name_member_first_name_member_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='image',
        ),
        migrations.RemoveField(
            model_name='member',
            name='image_id',
        ),
    ]
