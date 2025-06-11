from django.urls import path
from . import views

urlpatterns = [
    path('', views.municipality_view, name='municipality'),
    path('get_locations_json/', views.get_locations_json, name='get_locations_json'),  # <-- Asegura esta ruta
    # path('api/locations/', views.get_locations_json, name='get_locations'),
    path('save-location/', views.save_location, name='save_location'),
    path('location/', views.save_location, name='save_location'),
    path('create-quick-location/', views.create_quick_location, name='create_quick_location'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('add-popup/', views.add_popup, name='add_popup'),
    path('edit-popup/<int:location_id>/', views.edit_popup, name='edit_popup'),
    path('delete-popup/<int:location_id>/', views.delete_popup, name='delete_popup'),
    path('formNewMunicipality/', views.save_municipality, name='save_municipality'),
    path('formNewZone/', views.save_zone, name='save_zone'),
    path('get_locations_json/', views.get_locations_json, name='get_locations_json')
]