from rest_framework import serializers
from shops.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return {
          'm': obj.distance.m,
          'km': obj.distance.km
        }

    def get_location(self, obj):
        return [obj.location.y, obj.location.x]

    class Meta:
        model = Shop
        fields = ("name", "location", "address", "city", "distance")
