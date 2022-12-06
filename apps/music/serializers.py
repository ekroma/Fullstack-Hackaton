
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from apps.base.services import delete_old_file
from .models import (
    Track,
    PlayList,
    Genre,
    TrackImage,
    Like
)

class TrackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackImage
        fields = 'image', 


class TrackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Track
        fields = ('slug','image', 'title')

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']


    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.all().count()
        representation['liked_by'] = LikeSerializer(
            instance.likes.all().only('user'), many=True).data
        return representation

class TrackListSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('slug','image', 'title', 'file')

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']

class PlayListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = PlayList
        fields = '__all__'

    def validate_title(self, title):
        a = 1
        ex = f'{title}{a}'
        while PlayList.objects.filter(title=title).exists():
            a += 1
            ex = f'{title}{a}'
        title = ex
        return title

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name')


# class AlbumSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ('id', 'name', 'cover')
    
#     def update(self, instance, validated_data):
#         delete_old_file(instance.cover.path)
#         return super().update(instance, validated_data)

class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('id', 'title', 'tracks')
    
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)

class CurrentTrackDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['track']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    track = serializers.HiddenField(default=CurrentTrackDefault())
    
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        track = self.context.get('track').pk
        like = Like.objects.filter(user=user, track=track).first()
        if like:
            raise serializers.ValidationError('Already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        track = self.context.get('track').pk
        like = Like.objects.filter(user=user, track=track).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('Not liked yet')