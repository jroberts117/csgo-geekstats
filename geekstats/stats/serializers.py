from rest_framework import serializers

class MapSerializer(serializers.Serializer):
    map_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    rating = serializers.IntegerField()

class MapImageSerializer(serializers.Serializer):
    mid = serializers.IntegerField()
    type = serializers.CharField()
    image = serializers.ImageField()

class DataSerializer(serializers.Serializer):
    did = serializers.IntegerField()
    field = serializers.CharField()
    value = serializers.CharField()
    uid = serializers.CharField()

class MapRequestSerializer(serializers.Serializer):
    mid = serializers.IntegerField()
    map = serializers.CharField()
    type = serializers.CharField()

class AIRequestSerializer(serializers.Serializer):
    type = serializers.CharField()
    season_name = serializers.CharField()
    spec_inst = serializers.CharField()

class StatRequestSerializer(serializers.Serializer):
    player = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
