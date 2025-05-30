from django.urls import path
from . import views


urlpatterns = [
    path('', views.users),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('areaStaff/', views.users, name='staff')
]