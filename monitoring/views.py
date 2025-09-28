from django.shortcuts import render
from django.http import JsonResponse
from .models import CropData
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from django.utils import timezone

def dashboard_home(request):
    # Auto-create sample data if none exists
    if CropData.objects.count() == 0:
        create_sample_data()
    
    latest_data = CropData.objects.order_by('-timestamp').first()
    
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
    # Auto-create sample data if none exists  
    if CropData.objects.count() == 0:
        create_sample_data()
        
    # Get data from last 24 hours
    cutoff_time = timezone.now() - timedelta(hours=24)
    queryset = CropData.objects.filter(timestamp__gte=cutoff_time).order_by('timestamp')
    
    data = {
        'timestamps': [item.timestamp.strftime('%H:%M') for item in queryset],
        'soil_moisture': [float(item.soil_moisture) for item in queryset],
        'soil_ph': [float(item.soil_ph) for item in queryset],
        'vpd': [float(item.vpd) for item in queryset],
        'light_intensity': [float(item.light_intensity)/1000 for item in queryset],  # Convert to klux
    }
    
    return JsonResponse(data)

def create_sample_data():
    """Create sample agricultural data for demonstration"""
    import random
    
    crops_data = [
        {'name': 'Tomato', 'stage': 'harvest'},
        {'name': 'Cucumber', 'stage': 'flowering'}, 
        {'name': 'Lettuce', 'stage': 'vegetative'},
        {'name': 'Pepper', 'stage': 'fruiting'},
    ]
    
    # Create 24 hours of sample data
    for i in range(24):
        crop = random.choice(crops_data)
        CropData.objects.create(
            crop_name=crop['name'],
            crop_stage=crop['stage'],
            soil_moisture=random.uniform(75, 85),
            soil_ec=random.uniform(1.4, 1.8),
            soil_ph=random.uniform(6.2, 6.8),
            vpd=random.uniform(1.0, 1.3),
            light_intensity=random.uniform(45000, 55000),
            timestamp=timezone.now() - timedelta(hours=i)
        )
