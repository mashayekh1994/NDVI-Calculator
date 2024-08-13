# # management/commands/update_ndvi.py

# from django.core.management.base import BaseCommand
# from NDVI.models import MonitoringArea, NDVIResult
# import ee
# from datetime import datetime

# ee.Initialize()

# class Command(BaseCommand):
#     help = 'Fetch and process latest satellite imagery for monitoring areas'

#     def handle(self, *args, **kwargs):
#         monitoring_areas = MonitoringArea.objects.all()

#         for area in monitoring_areas:
#             aoi = ee.Geometry.Polygon(area.area.coords[0])
#             sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
#                           .filterBounds(aoi) \
#                           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
#                           .sort('system:time_start', False)

#             latest_image = sentinel2.first()
#             if latest_image:
#                 ndvi = latest_image.normalizedDifference(['B8', 'B4']).rename('NDVI')
#                 ndvi_clipped = ndvi.clip(aoi)

#                 ndvi_url = ndvi_clipped.getThumbURL({'min': 0, 'max': 1, 'dimensions': '1024x1024', 'palette': ['red', 'yellow', 'green']})
#                 min_ndvi = ndvi_clipped.reduceRegion(ee.Reducer.min(), aoi, 10).get('NDVI').getInfo()
#                 max_ndvi = ndvi_clipped.reduceRegion(ee.Reducer.max(), aoi, 10).get('NDVI').getInfo()
#                 capture_date = datetime.utcfromtimestamp(latest_image.get('system:time_start').getInfo() / 1000)

#                 NDVIResult.objects.create(
#                     area=area,
#                     capture_date=capture_date,
#                     ndvi_image_url=ndvi_url,
#                     min_ndvi=min_ndvi,
#                     max_ndvi=max_ndvi
#                 )
#                 self.stdout.write(self.style.SUCCESS(f'Successfully updated NDVI for {area.name}'))


# management/commands/update_ndvi.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from NDVI.models import MonitoringArea, NDVIResult
import ee

ee.Initialize()

class Command(BaseCommand):
    help = 'Fetch and process latest satellite imagery for monitoring areas'

    def handle(self, *args, **kwargs):
        monitoring_areas = MonitoringArea.objects.all()

        for area in monitoring_areas:

            # Definition of geographic area
            aoi = ee.Geometry.Polygon(area.area.coords[0])

            # Collecting Sentinel satellite image 2
            sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
                          .filterBounds(aoi) \
                          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                          .sort('system:time_start', False)

            latest_image = sentinel2.first()

            if latest_image:
                # Calculate NDVI
                ndvi = latest_image.normalizedDifference(['B8', 'B4']).rename('NDVI')
                ndvi_clipped = ndvi.clip(aoi)

                # Recieve URL of NDVI images
                ndvi_url = ndvi_clipped.getThumbURL({
                    'min': 0, 
                    'max': 1, 
                    'dimensions': '1024x1024', 
                    'palette': ['red', 'yellow', 'green']
                })

                # calculate min and max NDVI
                min_ndvi = ndvi_clipped.reduceRegion(
                    reducer=ee.Reducer.min(), 
                    geometry=aoi, 
                    scale=10
                ).get('NDVI').getInfo()

                max_ndvi = ndvi_clipped.reduceRegion(
                    reducer=ee.Reducer.max(), 
                    geometry=aoi, 
                    scale=10
                ).get('NDVI').getInfo()

                # create results on database
                NDVIResult.objects.create(
                    area=area,
                    capture_date=timezone.now(),
                    ndvi_image_url=ndvi_url,
                    min_ndvi=min_ndvi,
                    max_ndvi=max_ndvi
                )

                self.stdout.write(self.style.SUCCESS(f'Successfully updated NDVI for {area.name}'))
