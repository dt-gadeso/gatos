from django.urls import path
from . import views
from .views import AssociationCreateView


urlpatterns = [
    path('', views.association),
    path('asignar/', AssociationCreateView.as_view(), name='association'),
]