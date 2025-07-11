from django.contrib import admin
from django.urls import path, include, re_path
from users import views
from django.conf import settings
from django.conf.urls.static import static
from home.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'), name='home'),
    path('veterinarian/', include('veterinarian.urls'), name='veterinarian'),
    path('cats/', include('cats.urls'), name='cats'),
    path('colonies/', include('colonies.urls'), name='colonies'),
    path('users/', include('users.urls'), name='users'),
    # Catch-all pattern para URLs no encontradas
    re_path(r'^.*/$', custom_404, name='catch_all'),
]

# Handler para error 404
handler404 = 'home.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)