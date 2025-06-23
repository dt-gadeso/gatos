from django.urls import path
from . import views

urlpatterns = [
    path('', views.veterinarian, name='veterinarian'),
    path('formNewVetCenter/', views.vetcenter_form_view, name='formNewVetCenter'),
    path('formNewAgreement/', views.agreement_form_view, name='formNewAgreement'),
    path('formNewVetService/', views.vetservice_form_view, name='formNewVetService'),
    path('formNewVisit/', views.visit_form_view, name='formNewVisit'),
    path('formNewVisitService/', views.visitservice_form_view, name='formNewVisitService'),
]