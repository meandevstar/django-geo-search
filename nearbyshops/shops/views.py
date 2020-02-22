from django.shortcuts import render
from django.views import generic
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from .models import Shop

longitude = 54.967302
latitude = 37.313515

user_location = Point(longitude, latitude, srid=4326)

class ShopListAPIView(generic.ListView):
    model = Shop
    context_object_name = 'shops'
    queryset = Shop.objects.annotate(distance=Distance('location', user_location)) \
    	.order_by('distance')[0:10]
    template_name = 'shops/index.html'
