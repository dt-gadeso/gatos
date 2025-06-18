from django.contrib import admin
from django.urls import path, include
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),
    path('veterinarian/', include('veterinarian.urls'), name='veterinarian'),
    path('cats/', include('cats.urls'), name='cats'),
    path('colonies/', include('colonies.urls'), name='colonies'),
    path('users/', include('users.urls'), name='users')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)