from django.urls import path
from . import views
from .views import CatListView, CatUpdateView

urlpatterns = [
    path('', views.cat, name='cats'),
    path('formNewCat/', views.newCat, name='formNewCat'),
    path('formEditCat/<str:chip>/', views.editCat, name='formEditCat'),
    path('searchEditCat', views.searchEditCat, name='searchEditCat'),
    path('sterilized-counter/', views.sterilized_counter, name='sterilized_counter'),
    path('edit/<int:pk>/', CatUpdateView.as_view(), name='cat-edit'),
]