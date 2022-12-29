from rest_framework import serializers

class MapSerializer(serializers.Serializer):
    map_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    rating = serializers.IntegerField()

class MapImageSerializer(serializers.Serializer):
    mid = serializers.IntegerField()
    type = serializers.CharField()
    image = serializers.ImageField()