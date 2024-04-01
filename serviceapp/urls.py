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
    path('userrentsttaus/', views.userrentsttaus, name='userrentsttaus'),   
    path('adminservicedashboard/', views.adminservicedashboard, name='adminservicedashboard'),   
    path('adminserviceprovider/', views.adminserviceprovider, name='adminserviceprovider'),   
    path('rentpayment/<int:rent_id>/', views.rentpayment, name='rentpayment'),
    path('paymenthandlerrent/', views.paymenthandlerrent, name='paymenthandlerrent'),
    path('add_to_compare/<int:product_id>/', views.add_to_compare, name='add_to_compare'),
    path('compare/', views.compare_properties, name='compare_properties'),
    path('remove_property/<int:product_id>/', views.remove_property, name='remove_property'),
    path('servicepayment/<int:service_id>/', views.servicepayment, name='servicepayment'),
    path('paymenthandlerservice/', views.paymenthandlerservice, name='paymenthandlerservice'),
    path('checkassignments/', views.checkassignments, name='checkassignments'),
    path('takedelivery/<int:t_id>/', views.takedelivery, name='takedelivery'),
    path('deliverydone/<int:t_id>/', views.deliverydone, name='deliverydone'),
    path('myassignments/', views.myassignments, name='myassignments'),
    path('feedback_page/<int:ser_id>/', views.feedback_page, name='feedback_page'),
    path('add_comment/<int:ser_id>', views.add_comment, name='add_comment'),
    path('delete_feedback/<int:feedback_id>/<int:ser_id>/', views.delete_feedback, name='delete_feedback'),
    path('servicebooking', views.servicebooking, name='servicebooking'),
    path('get_bookings_for_date/', views.get_bookings_for_date, name='get_bookings_for_date'),
    path('servicelanding', views.servicelanding, name='servicelanding'),

    
    
    


    







    



    
    

    





    

    
]