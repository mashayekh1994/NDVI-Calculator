from django.contrib.gis.db import models as gis_models
from django.db import models

class MonitoringArea(models.Model):
    name = models.CharField(max_length=100)
    area = gis_models.PolygonField()

    def __str__(self):
        return self.name

class NDVIResult(models.Model):
    area = models.ForeignKey(MonitoringArea, on_delete=models.CASCADE)
    capture_date = models.DateTimeField()
    ndvi_image_url = models.URLField(max_length=500)
    min_ndvi = models.FloatField(null=True, blank=True)
    max_ndvi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"NDVI on {self.capture_date} for {self.area.name}"
