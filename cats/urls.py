from django.urls import path
from . import views

urlpatterns = [
    path('', views.cat, name='cats'),
    path('formNewCat/', views.newCat, name='formNewCat')
]