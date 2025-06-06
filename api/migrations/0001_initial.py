# Generated by Django 5.2.1 on 2025-05-11 03:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('album', models.CharField(blank=True, max_length=100, null=True)),
                ('genre', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
                ('duration', models.DurationField()),
                ('language', models.CharField(max_length=50)),
                ('audio_quality', models.CharField(max_length=20)),
                ('bitrate', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('play_count', models.IntegerField(default=0)),
                ('cover_art', models.ImageField(blank=True, null=True, upload_to='cover_arts/')),
                ('featured_artists', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('file_format', models.CharField(max_length=10)),
                ('song_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('songs', models.ManyToManyField(to='api.song')),
            ],
        ),
    ]
