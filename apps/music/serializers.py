from rest_framework import serializers
from .models import Track


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
