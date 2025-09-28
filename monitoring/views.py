from django.shortcuts import render
from django.http import JsonResponse
from .models import CropData
from django.db.models import Avg, Count
from datetime import datetime, timedelta

def dashboard_home(request):
    # Get latest readings
    latest_data = CropData.objects.first()
    
    # Get average values for the last 24 hours
    yesterday = datetime.now() - timedelta(days=1)
    avg_data = CropData.objects.filter(
        timestamp__gte=yesterday
    ).aggregate(
        avg_moisture=Avg('soil_moisture'),
        avg_ec=Avg('soil_ec'),
        avg_ph=Avg('soil_ph'),
        avg_vpd=Avg('vpd'),
        avg_light=Avg('light_intensity')
    )
    
    # Get crop stage distribution
    stage_data = CropData.objects.values('crop_stage').annotate(
        count=Count('id')
    )
    
    context = {
        'latest_data': latest_data,
        'avg_data': avg_data,
        'stage_data': stage_data,
    }
    
    return render(request, 'dashboard/home.html', context)

def api_chart_data(request):
    # Get last 24 hours of data for charts
    yesterday = datetime.now() - timedelta(days=1)
    data = CropData.objects.filter(timestamp__gte=yesterday).order_by('timestamp')
    
    chart_data = {
        'timestamps': [item.timestamp.strftime('%H:%M') for item in data],
        'soil_moisture': [item.soil_moisture for item in data],
        'soil_ec': [item.soil_ec for item in data],
        'soil_ph': [item.soil_ph for item in data],
        'vpd': [item.vpd for item in data],
        'light_intensity': [item.light_intensity for item in data],
    }
    
    return JsonResponse(chart_data)
