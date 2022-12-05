from rest_framework import serializers
from .models import (
    Rating,
    Like
)

class CurrentTrackDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['post']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    post = serializers.HiddenField(default=CurrentTrackDefault())
    
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


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )


    class Meta:
        model = Rating
        fields = ('rating', 'user', 'track')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)
