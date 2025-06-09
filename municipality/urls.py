from django.urls import path
from . import views

urlpatterns = [
    path('', views.municipality_view, name='municipality'),
    path('api/locations/', views.get_locations_json, name='get_locations'),
    path('api/save-location/', views.save_location, name='save_location'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
]