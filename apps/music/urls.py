from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, PlayListViewSet, RetrieveTrackView, Trackist


router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')
router.register('playlists', PlayListViewSet, 'playlists')

urlpatterns = [
    path('tracks/', Trackist.as_view(), name='track_list'),
    path('tracks/<str:pk>/', RetrieveTrackView.as_view(), name='retrieve')
]

urlpatterns += router.urls
