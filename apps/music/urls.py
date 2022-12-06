from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LikedPostsView, TrackViewSet, PlayListViewSet # RetrieveTrackView, TrackList


router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')
router.register('playlists', PlayListViewSet, 'playlists')


urlpatterns = [
    path('liked/', LikedPostsView.as_view(), name='liked'),
    # path('tracks/', TrackList.as_view(), name='track_list'),
    # path('tracks/<str:pk>/', RetrieveTrackView.as_view(), name='retrieve')

]

urlpatterns += router.urls
