# Generated by Django 4.1.3 on 2022-12-06 11:25

import apps.base.services
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('name', models.SlugField(max_length=35, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='Title')),
                ('image', models.ImageField(upload_to='playlist_image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), apps.base.services.validate_image_size])),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('file', models.FileField(upload_to=apps.base.services.get_upload_path_track, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])], verbose_name='Track')),
                ('slug', models.SlugField(blank=True, max_length=220, primary_key=True, serialize=False, verbose_name='Slug')),
                ('image', models.ImageField(upload_to='track_image', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), apps.base.services.validate_image_size])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(blank=True, max_length=100, verbose_name='Author')),
                ('genre', models.ManyToManyField(related_name='genre', to='music.genre')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='TrackImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='track_images')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='music.track')),
            ],
        ),
        migrations.CreateModel(
            name='PlayListImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='playlist_images')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='music.playlist')),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(related_name='playlist_tracks', to='music.track'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='play_lists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='music.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
