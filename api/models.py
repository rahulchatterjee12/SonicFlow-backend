from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100, null=True, blank=True)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    duration = models.DurationField()
    language = models.CharField(max_length=50)
    audio_quality = models.CharField(max_length=20)
    bitrate = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    play_count = models.IntegerField(default=0)
    cover_art = models.ImageField(upload_to='cover_arts/', null=True, blank=True)
    file_format = models.CharField(max_length=10)
    song_url = models.URLField()

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"
