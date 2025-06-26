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
    path('associations/', views.association_list, name='association_list'),
    path('associations/create/', views.association_create, name='association_create'),
    path('search_users/', views.search_users, name='search_users'),
    path('search_associations/', views.search_associations, name='search_associations'),
    path('admin_delete_user/', views.admin_delete_user, name='admin_delete_user'),
]