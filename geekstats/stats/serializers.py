from rest_framework import serializers

class MapSerializer(serializers.Serializer):
    map_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    rating = serializers.IntegerField()