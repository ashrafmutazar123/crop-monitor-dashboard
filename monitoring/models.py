from django.db import models
from django.utils import timezone

class CropData(models.Model):
    CROP_STAGES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('harvest', 'Harvest Ready'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    crop_name = models.CharField(max_length=100)
    crop_stage = models.CharField(max_length=20, choices=CROP_STAGES)
    soil_moisture = models.FloatField(help_text="Soil moisture percentage")
    soil_ec = models.FloatField(help_text="Electrical conductivity (mS/cm)")
    soil_ph = models.FloatField(help_text="pH level")
    vpd = models.FloatField(help_text="Vapor Pressure Deficit (kPa)")
    light_intensity = models.FloatField(help_text="Light intensity (lux)")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.crop_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
