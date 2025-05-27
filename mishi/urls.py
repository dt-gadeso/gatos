from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),
    path('veterinarian/', include('veterinarian.urls'), name='veterinarian'),
    path('cats/', include('cats.urls'), name='cats'),
    path('colonies/', include('colonies.urls'), name='colonies'),
    path('association/', include('association.urls'), name='association'),
    path('municipality/', include('municipality.urls'), name='municipality'),
    path('users/', include('users.urls'), name='users'),
]
