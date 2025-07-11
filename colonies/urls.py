from django.urls import path
from . import views

urlpatterns = [
    path('', views.colonies_view, name='colonies'),
    path('get_locations_json/', views.get_locations_json, name='get_locations_json'),
    path('save-location/', views.save_location, name='save_location'),
    path('location/', views.save_location, name='save_location'),
    path('create-quick-location/', views.create_quick_location, name='create_quick_location'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('formNewMunicipality/', views.save_municipality, name='save_municipality'),
    path('formNewZone/', views.save_zone, name='save_zone'),
    path('formNewCouncil/', views.save_council, name='save_council'),
    path('formNewColony/', views.new_colony, name='new_colony'),
    path('formNewIncident/', views.save_incident, name='save_incident'),
    path('formEditIncident/<int:incident_id>/', views.editIncident, name='editIncident'),
    path('incidents/search/', views.searchIncidents, name='searchIncidents'),
    path('incident_search_result/', views.searchIncidents, name='incident_search_result'),
    path('formularios_multiples/', views.multi_form_view, name='multi_forms'),
]

handler404 = 'colonies.views.mi_error_404'