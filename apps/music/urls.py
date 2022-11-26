from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet


router = DefaultRouter()
router.register('tracks', TrackViewSet, 'tracks')

urlpatterns = []

urlpatterns += router.urls