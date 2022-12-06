import os
from rest_framework import filters
from django_filters import rest_framework as rest_filter
# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
# from django.http import FileResponse, Http404, HttpResponse
# from django.shortcuts import get_object_or_404
from .permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAdminUser, 
    AllowAny
    )

from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from .serializers import (
    CreatePlayListSerializer,
    TrackListSerialiers, 
    TrackSerializer,
    GenreSerializer
    ) 

from .models import Track, PlayList, Genre


class TrackList(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackListSerialiers
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user__username']
    filterset_fields = ['genre']
    ordering_fields = ['plays']


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TrackListSerialiers
        return TrackSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class GenreView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayListViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, )
    queryset = PlayList.objects.all()
    serializer_class = CreatePlayListSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()


# class RetrieveTrackView(APIView):

#     def get(self, request, pk):
#         track = get_object_or_404(Track, slug=pk)
#         if os.path.exists(track.file.path):
#             # self.set_play()
#             #response = HttpResponse('', content_type="audio/mpeg", status=206)
#             #response['X-Accel-Redirect'] = f"/mp3/{track.file.name}"
#             response = FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
#             # track_img = FileResponse(open(track.image.path, 'rb'), filename=track.image.name)
#             # response = {'track':track_file, 'image': track_img}
#             return response
#         else:
#             return Http404


