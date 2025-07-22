from django.urls import path
from . import views

urlpatterns = [
    path('', views.veterinarian, name='veterinarian'),
    path('formNewVetCenter/', views.vetcenter_form_view, name='formNewVetCenter'),
    path('formNewVisit/', views.visit_form_view, name='formNewVisit'),
    path('search/', views.search_vet_centers, name='search_vet_centers'),
]