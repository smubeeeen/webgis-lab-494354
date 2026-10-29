from django.contrib.gis.geos import Point
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import District


def map_page(request):
    provinces = (District.objects.order_by("province")
                 .values_list("province", flat=True).distinct())
    return render(request, "districts/map.html", {"provinces": provinces})


def districts_geojson(request):
    districts = District.objects.all()

    # /api/districts/?province=Sindh -> only that province (filtered in PostGIS)
    province = request.GET.get("province")
    if province:
        districts = districts.filter(province=province)

    data = serialize(
        "geojson",
        districts,
        geometry_field="geom",
        fields=["name", "province", "pop_2023", "area_km2"],
    )
    return HttpResponse(data, content_type="application/geo+json")


# Part 8 (extension): which district is this point in?
def district_at(request):
    try:
        lat = float(request.GET["lat"])
        lng = float(request.GET["lng"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "give lat and lng as numbers"}, status=400)

    point = Point(lng, lat, srid=4326)   # GEOS wants x (lng) first
    district = District.objects.filter(geom__contains=point).first()

    if district is None:
        return JsonResponse({"district": None})
    return JsonResponse({
        "district": district.name,
        "province": district.province,
        "pop_2023": district.pop_2023,
    })
