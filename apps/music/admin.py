from django.contrib import admin
from .models import Track, TrackImage, Genre, PlayList, Like

class TabularInlineImage(admin.TabularInline):
    model = TrackImage
    extra = 0
    fields = ['image']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    inlines = [TabularInlineImage, ]
    list_display = ('slug','user', 'title', 'created_at')
    list_display_links = ('user',)
    list_filter = ('genre', 'created_at')
    search_fields = ('user', 'genre__name')

@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user')
    list_display_links = ('user',)
    search_fields = ('user', 'tracks__name')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'track')
    list_display_links = ('user','track')

    