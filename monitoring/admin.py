from django.contrib import admin
from .models import CropData

@admin.register(CropData)
class CropDataAdmin(admin.ModelAdmin):
    list_display = ['crop_name', 'crop_stage', 'soil_moisture', 'soil_ph', 'timestamp']
    list_filter = ['crop_stage', 'crop_name', 'timestamp']
    search_fields = ['crop_name']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Crop Information', {
            'fields': ('crop_name', 'crop_stage', 'timestamp')
        }),
        ('Soil Parameters', {
            'fields': ('soil_moisture', 'soil_ec', 'soil_ph')
        }),
        ('Environmental Parameters', {
            'fields': ('vpd', 'light_intensity')
        }),
    )
