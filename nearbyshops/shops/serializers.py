from rest_framework import serializers
from shops.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return obj.distance.m

    def get_location(self, obj):
        return [obj.location.x, obj.location.y]

    class Meta:
        model = Shop
        fields = ("name", "location", "address", "city", "distance")
