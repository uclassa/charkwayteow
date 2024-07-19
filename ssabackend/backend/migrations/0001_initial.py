# Generated by Django 5.0.1 on 2024-07-16 19:16

import backend.models
import django.db.models.deletion
import gdstorage.storage
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(blank=True, null=True, verbose_name='Image id (do not edit)')),
                ('image', models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=backend.models._get_upload_path)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('telegram_username', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('telegram_id', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('gender', models.CharField(blank=True, max_length=10)),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='backend.family')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(blank=True, null=True, verbose_name='Image id (do not edit)')),
                ('image', models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=backend.models._get_upload_path)),
                ('title', models.CharField(max_length=30)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('venue', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('participants', models.ManyToManyField(blank=True, related_name='events', to='backend.member')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhotoSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(blank=True, null=True, verbose_name='Image id (do not edit)')),
                ('image', models.ImageField(blank=True, null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=backend.models._get_upload_path)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('score', models.FloatField(default=0)),
                ('description', models.TextField(blank=True)),
                ('number_of_people', models.IntegerField(default=0)),
                ('family', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photo_submissions', to='backend.family')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='photo_submissions', to='backend.member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
