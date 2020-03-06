from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F, Sum
from .models import Shop
from .serializers import ShopSerializer

DEFAULT_LON = 13.348943
DEFAULT_LAT = 52.524323
DEFAULT_COUNT = 10

class ShopListAPIView(RetrieveAPIView):
    model = Shop
    serializer_class = ShopSerializer

    def retrieve(self, request, *args, **kwargs):
        lat = float(self.request.GET.get("lat", DEFAULT_LAT))
        lon = float(self.request.GET.get("lon", DEFAULT_LON))
        limit = self.request.query_params.get("limit", 10)
        page_no = int(self.request.query_params.get("pageNo", 0)) + 1
        order = self.request.query_params.get("order")
        order_by = self.request.query_params.get("orderBy")
        user_location = Point(lon, lat, srid=4326)

        shops = Shop.objects \
            .annotate(distance=Distance('location', user_location)) \
            .order_by('distance')

        if order is not None and order_by is not None:
            shops = shops.order_by(order_by)

            if order == "desc":
                shops = shops.reverse()

        paginator = Paginator(shops, limit)
        try:
            data = paginator.page(page_no)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serialized = []
        for v in data:
            serialized.append(ShopSerializer(v).data)

        result = {
            "data": serialized,
            "total": shops.count()
        }
        return Response(data=result, status=status.HTTP_200_OK)

