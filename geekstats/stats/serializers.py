from rest_framework import serializers
from datetime import date
from django.utils import timezone

class MapSerializer(serializers.Serializer):
    map_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    rating = serializers.IntegerField()

class BotMapSerializer(serializers.Serializer):
    map = serializers.CharField()
    user = serializers.CharField()
    rating = serializers.IntegerField()
    key = serializers.CharField(default="none")

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

def get_current_date():
    return timezone.now().date()

class StatRequestSerializer(serializers.Serializer):
    current_date = timezone.now().date()
    player = serializers.CharField(default="none")
    start_date = serializers.DateField(default=current_date)
    end_date = serializers.DateField(default=current_date)
    season = serializers.CharField(default="none")
    cap1 = serializers.CharField(default="none")
    cap2 = serializers.CharField(default="none")
    type = serializers.CharField(default="none")


