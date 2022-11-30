from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, PlayListViewSet


router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')
router.register('playlists', PlayListViewSet, 'playlists')

urlpatterns = []

urlpatterns += router.urls