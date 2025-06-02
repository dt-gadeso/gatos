from django.urls import path
from . import views

urlpatterns = [
    path('', views.cat, name='cats'),
    path('formNewCat/', views.newCat, name='formNewCat'),
    path('formEditCat/<str:chip>/', views.editCat, name='formEditCat'),
    path('searchEditCat', views.searchEditCat, name='searchEditCat'),
    ]