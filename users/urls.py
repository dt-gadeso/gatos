from django.urls import path
from . import views
from .views import Staff

urlpatterns = [
    path('', Staff.as_view()),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('areaStaff/', Staff.as_view(), name='areaStaff'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('areaEdit/', views.areaEdit, name='areaEdit'),
    path('role/', views.assign_role, name='assign_role'),
]