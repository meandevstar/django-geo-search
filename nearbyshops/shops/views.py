from django.views import generic
from django.shortcuts import render
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F, Sum
from .models import Shop

DEFAULT_LON = 13.348943
DEFAULT_LAT = 52.524323
DEFAULT_COUNT = 10

class ShopListAPIView(generic.ListView):
    model = Shop

    def get_context_data(self, **kwargs):
        count = int(self.request.GET.get("count", DEFAULT_COUNT))
        lat = float(self.request.GET.get("lat", DEFAULT_LAT))
        lon = float(self.request.GET.get("lon", DEFAULT_LON))
        user_location = Point(lon, lat, srid=4326)

        print(count, lat, lon)
        
        context = super(ShopListAPIView, self).get_context_data(**kwargs)

        context['shops'] = Shop.objects \
            .annotate(distance=Distance('location', user_location)) \
            .order_by('distance')[0:count]

        context['query'] = {
            'lat': lat,
            'lon': lon,
            'count': count
        }

        return context