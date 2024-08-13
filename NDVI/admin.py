from django.contrib import admin
from .models import NDVIResult, MonitoringArea
from leaflet.admin import LeafletGeoAdmin

@admin.register(MonitoringArea)
class MonitoringAreaAdmin(LeafletGeoAdmin):
    list_display = ('name', 'get_area_coords')
    search_fields = ('name',)

    def get_area_coords(self, obj):
        return obj.area.wkt
    get_area_coords.short_description = 'Area Coordinates'


    
from django.utils.html import format_html

@admin.register(NDVIResult)
class NDVIResultAdmin(admin.ModelAdmin):
    list_display = ('area', 'capture_date', 'ndvi_image_preview')
    readonly_fields = ('ndvi_map_display',) 

    def ndvi_image_preview(self, obj):
        if obj.ndvi_image_url:
            return format_html('<img src="{}" style="width: 200px; height: auto;" />', obj.ndvi_image_url)
        return "No Image"

    ndvi_image_preview.short_description = "NDVI Image Preview"

    def ndvi_map_display(self, obj):
        if obj.ndvi_image_url:
            return format_html('<img src="{}" style="max-width: 100%; height: auto;" />', obj.ndvi_image_url)
        return "No Image"

    ndvi_map_display.short_description = "NDVI Map"

