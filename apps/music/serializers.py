from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from apps.base.services import delete_old_file
from .models import Track, PlayList, Genre, TrackImage
from django.shortcuts import get_object_or_404


class TrackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackImage
        fields = 'image', 


class TrackSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Track
        fields = ('slug','image', 'title')

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep['carousel'] = TrackImageSerializer(
    #         instance.smart_images.all(), many=True).data
    #     # rating = instance.ratings.aggregate(Avg('rating'))['rating__avg']
    #     rep['likes'] = instance.likes.all().count()
    #     # rep['liked_by'] = LikeSerializer(
    #     #     instance.likes.all().only('user'), many=True).data
    #     # if rating:
    #     #     rep['rating'] = round(rating, 1)
    #     # else:
    #     #     rep['rating'] = 0.0
    #     # return rep

class TrackListSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('slug','image', 'title')

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']

    def to_representation(self, instance):
        # self.track = get_object_or_404(Track, slug=Track.slug)
        rep = super().to_representation(instance) 
        print('{{{{{{{',rep)
        # rep['image'] = instance
        return rep

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.image.path)
        return super().update(instance, validated_data)


class TrackCreateSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = '__all__'

    def create(self, validated_data):
        track = Track.objects.create(**validated_data)
        images = []
        TrackImage.objects.create(images)
        return track   

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


class CreatePlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields = ('id', 'title', 'tracks')
    
    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)