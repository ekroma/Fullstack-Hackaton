from django.contrib import admin
from .models import Track, TrackImage


class TabularInlineImage(admin.TabularInline):
    model = TrackImage
    extra = 0
    fields = ['image']


class TrackAdmin(admin.ModelAdmin):
    model = Track
    inlines = [TabularInlineImage, ]


admin.site.register(Track, TrackAdmin)