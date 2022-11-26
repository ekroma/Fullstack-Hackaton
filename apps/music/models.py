from django.db import models
from .utils import get_time
from slugify import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Track(models.Model):
    title = models.CharField('Title', max_length=200)
    track = models.FileField('Track', upload_to='tracks')
    # author = models.CharField('Author', max_length=100, blank=True)
    slug = models.SlugField('Slug', max_length=220, primary_key=True, blank=True)
    image = models.ImageField('Image', upload_to='track_images')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        verbose_name='Автор',
        to=User,
        on_delete=models.CASCADE,
        related_name='track'
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('track-detail', kwargs={'pk': self.pk})


class TrackImage(models.Model):
    image = models.ImageField(upload_to='track_images')
    laptop = models.ForeignKey(
        to=Track,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self) -> str:
        return f'Image to {self.product.title}'