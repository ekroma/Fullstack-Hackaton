from rest_framework import serializers

from apps.base.services import delete_old_file
from .models import Album, Track, PlayList, Genre

class TrackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Track
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)   
        return rep

class TrackListSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('image', 'title', 'slug')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

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


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'cover')
    
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)

class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('id', 'title', 'tracks')
    
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)
