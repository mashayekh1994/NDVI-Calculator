from django.shortcuts import render
from .models import MonitoringArea, NDVIResult
from django.shortcuts import render, redirect, get_object_or_404
from .models import MonitoringArea
from .forms import MonitoringAreaForm
from .models import NDVIResult, MonitoringArea

def ndvi_map(request):
    areas = MonitoringArea.objects.all()
    return render(request, 'ndvi_map.html', {'areas': areas})


def ndvi_results_list(request):
    ndvi_results = NDVIResult.objects.all().order_by('-capture_date')
    return render(request, 'ndvi_results_list.html', {'ndvi_results': ndvi_results})

def ndvi_result_detail(request, pk):
    ndvi_result = get_object_or_404(NDVIResult, pk=pk)
    return render(request, 'ndvi_result_detail.html', {'ndvi_result': ndvi_result})

def monitoring_area_ndvi_map(request, pk):
    monitoring_area = get_object_or_404(MonitoringArea, pk=pk)
    ndvi_results = NDVIResult.objects.filter(area=monitoring_area).order_by('-capture_date')

    # دریافت محدوده‌ها (bounds) از پایگاه داده یا محاسبه به صورت دستی
    area_bounds = monitoring_area.area.extent  # (xmin, ymin, xmax, ymax)
    
    return render(request, 'monitoring_area_ndvi_map.html', {
        'monitoring_area': monitoring_area,
        'ndvi_results': ndvi_results,
        'area_bounds': area_bounds,
    })




def monitoring_area_list(request):
    areas = MonitoringArea.objects.all()
    return render(request, 'monitoring_area_list.html', {'areas': areas})

def add_monitoring_area(request):
    if request.method == 'POST':
        form = MonitoringAreaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('monitoring_area_list')
    else:
        form = MonitoringAreaForm()
    return render(request, 'monitoring_area_form.html', {'form': form})

def edit_monitoring_area(request, pk):
    area = get_object_or_404(MonitoringArea, pk=pk)
    if request.method == 'POST':
        form = MonitoringAreaForm(request.POST, request.FILES, instance=area)
        if form.is_valid():
            form.save()
            return redirect('monitoring_area_list')
    else:
        form = MonitoringAreaForm(instance=area)
    return render(request, 'monitoring_area_form.html', {'form': form})

def delete_monitoring_area(request, pk):
    area = get_object_or_404(MonitoringArea, pk=pk)
    if request.method == 'POST':
        area.delete()
        return redirect('monitoring_area_list')
    return render(request, 'monitoring_area_confirm_delete.html', {'area': area})
