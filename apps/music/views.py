import os
from django_filters import rest_framework as filters
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
    TrackListSerialiers, 
    TrackSerializer,
    GenreSerializer,
    LikeSerializer,
    ) 

from .models import Track, PlayList, Genre

class Trackist(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackListSerialiers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('genre', 'author')
    search_fields = ['title', 'author']

class TrackViewSet(ModelViewSet):
    parser_classes =( MultiPartParser,)
    queryset = Track.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
        # if self.action == 'comment' and self.request.method == 'DELETE':
        #     self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    # @action(methods=['POST', 'PATCH'], detail=True, url_path='set_rating')
    # def set_rating(self, request, pk=None):
    #     data = request.data.copy()
    #     data['track'] = pk
    #     serializer = RatingSerializer(data=data, context={'request': request})
    #     rate = Rating.objects.filter(
    #         user=request.user,
    #         track=pk
    #     ).first()
    #     if serializer.is_valid(raise_exception=True):
    #         if rate and request.method == 'POST':
    #             return Response(
    #                 {'detail': 'Rating object exists. Use PATCH method'}
    #             )
    #         elif rate and request.method == 'PATCH':
    #             serializer.update(rate, serializer.validated_data)
    #             return Response('Updated')
    #         elif request.method == 'POST':
    #             serializer.create(serializer.validated_data)
    #             return Response(serializer.data)
    #         else:
    #             return Response({'detail': 'Rating object does not exist. Use POST method'})

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
        # if self.action == 'comment' and self.request.method == 'DELETE':
        #     self.permission_classes = [IsOwner]
        if self.action in ['create', 'comment', 'set_rating', 'like']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()

class RetrieveTrackView(APIView):
    """ Воспроизведение трека
    """
    # def set_play(self):
    #     self.track.plays_count += 1
    #     self.track.save()
    def get(self, request, pk):
        track = get_object_or_404(Track, slug=pk)
        if os.path.exists(track.file.path):
            # self.set_play()
            #response = HttpResponse('', content_type="audio/mpeg", status=206)
            #response['X-Accel-Redirect'] = f"/mp3/{track.file.name}"
            response = FileResponse(open(track.file.path, 'rb'), filename=track.file.name)
            # track_img = FileResponse(open(track.image.path, 'rb'), filename=track.image.name)
            # response = {'track':track_file, 'image': track_img}
            return response
        else:
            return Http404