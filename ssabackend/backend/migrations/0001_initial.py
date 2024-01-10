# Generated by Django 5.0.1 on 2024-01-10 00:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fam_name', models.CharField(max_length=30)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(max_length=10)),
                ('profile_image', models.ImageField(upload_to='')),
                ('family', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.family')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('venue', models.TextField()),
                ('description', models.TextField()),
                ('participants', models.ManyToManyField(related_name='events', to='backend.member')),
            ],
        ),
    ]
