from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
urlpatterns = [
    # Define your URL patterns here
    # Example:
    # path('', views.index, name='index'),
    path('update_status_accept/<int:t_id>/', views.update_status_accept, name='update_status_accept'),
    path('deliveryaddress/', views.deliveryaddress, name='deliveryaddress'),
    path('addressedit/<int:t_id>/', views.addressedit, name='addressedit'),
    path('adminrentdashboard/', views.adminrentdashboard, name='adminrentdashboard'),
    path('adminrentviewproducts/', views.adminrentviewproducts, name='adminrentviewproducts'),
    path('rentadminsingleview/<int:t_id>/', views.rentadminsingleview, name='rentadminsingleview'),
    path('admindeliveryagentsdashboard/', views.admindeliveryagentsdashboard, name='admindeliveryagentsdashboard'),
    path('adminproductandcategorydashboard/', views.adminproductandcategorydashboard, name='adminproductandcategorydashboard'),
    path('adminuserdashboard/', views.adminuserdashboard, name='adminuserdashboard'),
    path('adminreports/', views.adminreports, name='adminreports'),
    path('update_status_reject/<int:t_id>/', views.update_status_reject, name='update_status_reject'),
    path('adminrentrequest/', views.adminrentrequest, name='adminrentrequest'),
    path('userrentsttaus', views.userrentsttaus, name='userrentsttaus'),   


    
    

    





    

    
]