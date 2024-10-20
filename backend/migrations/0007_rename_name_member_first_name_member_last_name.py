# Generated by Django 5.0.7 on 2024-10-20 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_member_is_active_alter_photosubmission_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='member',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
