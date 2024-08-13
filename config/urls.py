
from django.contrib import admin
from django.urls import path
from NDVI.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ndvi-results/', ndvi_results_list, name='ndvi_results_list'),
    path('ndvi-result/<int:pk>/', ndvi_result_detail, name='ndvi_result_detail'),
    path('ndvi-result/<int:pk>/ndvi-map/', monitoring_area_ndvi_map, name='monitoring_area_ndvi_map'),

    path('monitoring-areas/', monitoring_area_list, name='monitoring_area_list'),
    path('monitoring-areas/add/', add_monitoring_area, name='add_monitoring_area'),
    path('monitoring-areas/edit/<int:pk>/', edit_monitoring_area, name='edit_monitoring_area'),
    path('monitoring-areas/delete/<int:pk>/', delete_monitoring_area, name='delete_monitoring_area'),

]
