import os
from rest_framework import filters
from django_filters import rest_framework as rest_filter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
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
    LikedPostSerializer,
    PlayList_ListSerialiers,
    PlayListSerializer,
    TrackListSerialiers, 
    TrackSerializer,
    GenreSerializer,
    LikeSerializer,
    ) 

from .models import Like, Track, PlayList, Genre


# class TrackList(ListAPIView):
#     queryset = Track.objects.all()
#     serializer_class = TrackListSerialiers
#     filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
#     search_fields = ['title', 'user__username']
#     filterset_fields = ['genre']
#     ordering_fields = ['plays']


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    filter_backends = [filters.SearchFilter, rest_filter.DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'user__username']
    filterset_fields = ['genre']
    ordering_fields = ['genre']

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
        if self.action in ['create', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, request, pk=None):
        track = self.get_object()
        serializer = LikeSerializer(data=request.data, context={
            'request': request,
            'track': track
        })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('Liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('Unliked!')

    # def retrieve(self, request, pk):
    #     res = super().retrieve(request, pk)
    #     track = get_object_or_404(Track, slug=pk)
    #     res['file'] =  FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
    #     return res

class GenreView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PlayListViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, )
    queryset = PlayList.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return PlayList_ListSerialiers
        if self.action == 'create':
            return CreatePlayListSerializer
        return PlayListSerializer


class LikedPostsView(ListAPIView):
    serializer_class = LikedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Like.objects.filter(user=user)


# class RetrieveTrackView(APIView):
#     # def set_play(self):
#     #     self.track.plays_count += 1
#     #     self.track.save()
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

