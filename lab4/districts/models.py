from django.contrib.gis.db import models


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    pcode = models.CharField(max_length=10, unique=True)
    # AJK, GB and Lehri have no 2023 census figure, so this can be empty
    pop_2023 = models.IntegerField(null=True, blank=True)
    area_km2 = models.FloatField()
    # MultiPolygon because some districts come in more than one piece
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        ordering = ["province", "name"]

    def __str__(self):
        return f"{self.name} ({self.province})"
