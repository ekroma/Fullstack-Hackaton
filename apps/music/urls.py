from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, PlayListViewSet, RetrieveTrackView


router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')
router.register('playlists', PlayListViewSet, 'playlists')

urlpatterns = [
    path('tracks/<str:pk>/', RetrieveTrackView.as_view(), name='streaming')
]

urlpatterns += router.urls