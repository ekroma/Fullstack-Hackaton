
from django.db import models

from apps.base.services import (
    get_upload_path_track_image, 
    validate_image_size, 
    get_upload_path_track
    )
from .utils import get_time
from slugify import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()


class Track(models.Model):
    title = models.CharField('Title', max_length=200)
    file = models.FileField(
        'Track', 
        upload_to=get_upload_path_track,
        validators=[FileExtensionValidator(allowed_extensions=['mp3','wav'])]
        )
    genre = models.ManyToManyField(
        to='Genre',
        related_name='genre'
    )
    slug = models.SlugField('Slug', max_length=220, primary_key=True, blank=True)
    image = models.ImageField(
        upload_to='track_image',
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_image_size],
        
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField('Author', max_length=100, blank=True)
    user = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        on_delete=models.CASCADE,
        related_name='track',
    )

    def save(self, *args, **kwargs):
        if not self.author:
            self.author = self.user.username
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("track-detail", kwargs={"pk": self.pk})
    

class TrackImage(models.Model):
    image = models.ImageField(upload_to='track_images')
    track = models.ForeignKey(
        to=Track,
        on_delete=models.CASCADE,
        related_name='images'
    )


class Genre(models.Model):
    name = models.SlugField(primary_key=True, max_length=35)

    def __str__(self):
        return self.name

class PlayList(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='play_lists'
    )
    title = models.CharField('Title',max_length=70)
    tracks = models.ManyToManyField(
        to=Track,
        related_name='playlist_tracks'
    )
    image = models.ImageField(
        upload_to='playlist_image',
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_image_size],
    )
    # trakci = models.ManyToManyField(to=Track,blank=True)

class PlayListImage(models.Model):
    image = models.ImageField(upload_to='playlist_images')
    track = models.ForeignKey(
        to=PlayList,
        on_delete=models.CASCADE,
        related_name='images'
    )


class Like(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    track = models.ForeignKey(
        to=Track,
        on_delete=models.CASCADE,
        related_name='likes'
    )


    def __str__(self) -> str:
        return f'Liked by {self.user.username}'

