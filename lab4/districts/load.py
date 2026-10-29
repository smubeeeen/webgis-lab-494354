"""Load data/districts.geojson into the District table.

Run with:
    python manage.py shell -c "from districts import load; load.run()"
"""
from pathlib import Path

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon

from .models import District

data_file = Path(__file__).resolve().parent.parent / "data" / "districts.geojson"


def run():
    layer = DataSource(data_file)[0]
    print(layer.name, ":", len(layer), "features,", layer.geom_type, "geometry")

    # empty the table first so the script can be re-run without duplicates
    District.objects.all().delete()

    wrapped = 0
    for feature in layer:
        geom = feature.geom.geos
        geom.srid = 4326

        # The file has 152 Polygons and 8 MultiPolygons. The column only takes
        # MultiPolygon, so a single polygon becomes a multipolygon of one part.
        if geom.geom_type == "Polygon":
            geom = MultiPolygon(geom, srid=4326)
            wrapped += 1

        District.objects.create(
            name=feature.get("district"),
            province=feature.get("province"),
            pcode=feature.get("pcode"),
            pop_2023=feature.get("pop_2023"),
            area_km2=feature.get("area_km2"),
            geom=geom,
        )

    print(wrapped, "polygons wrapped as multipolygons")
    print(District.objects.count(), "districts saved")
