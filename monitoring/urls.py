from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
]