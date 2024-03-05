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
from django.conf.urls.static import static
urlpatterns = [ 
    path('seminar2/', views.seminar2, name='seminar2'),
    
    path('result/', views.result, name='result'),
    path('addrent/', views.addrent, name='addrent'),
    path('rentuser/<int:t_id>/', views.rentuser, name='rentuser'),
    path('rentuserlist/', views.rentuserlist, name='rentuserlist'),
    path('services/', views.services, name='services'),
    path('manintenece/', views.manintenece, name='manintenece'),
    path('installation/', views.installation, name='installation'),
    path('spage/', views.spage, name='spage'),
    path('deliveryagentadmin/<int:appointment_id>/', views.deliveryagentadmin, name='deliveryagentadmin'),
    path('deliveryagentprofile/', views.deliveryagentprofile, name='deliveryagentprofile'),
    path('deliveryagentdashboard/', views.deliveryagentdashboard, name='deliveryagentdashboard'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get-available-time-slots'),
    path('listofservices/', views.listofservices, name='listofservices'),
    path('serviceadmin/', views.serviceadmin, name='serviceadmin'),
    path('requestpage/<int:appointment_id>/', views.requestpage, name='requestpage'),
    path('search_by_name/<str:name>/',views.searchByName,name="search_by_name"),
    path('deliverybase/', views.deliverybase, name='deliverybase'), 
    path('check_availability/', views.check_availability, name='check_availability'),
                            #to intrested people to regiter their interest
    path('admindeliveryagentviews/', views.admindeliveryagentviews, name='admindeliveryagentviews'),
    path('adminsidecatidacydelivery/', views.adminsidecatidacydelivery, name='adminsidecatidacydelivery'),   
                        #to intrested people to regiter their interest
                        
    path('acceptrent/<int:appointment_id>/', views.acceptrent, name='acceptrent'),   
    








]
