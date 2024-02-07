from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('regform/',views.userRegister,name='regform'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('seller/', views.seller, name='seller'),
    path('profile/', views.profile, name='profile'),
    path('sellerpage/', views.sellerpage, name='sellerpage'),
    path('updateproduct/<int:stid2>/', views.updateproduct, name='updateproduct'),
    path('product/', views.product, name='product'),
    path('register/', views.register, name='register'),
    path('accounts/', include('allauth.urls')),
    path('sellerprofile/', views.sellerprofile, name='sellerprofile'),
    path('category/', views.category, name='category'),
    path('sellerindex/', views.sellerindex, name='sellerindex'),
    path('categoryajax/<str:category>/', views.categoryajax, name='categoryajax'),
    path('addcategory/<int:stid2>/', views.update, name='addcategory'),
    path('deletecategory/<int:stid2>/',views.deletecategory, name='deletecategory'),
    path('deleteproduct/<int:stid2>/', views.deleteproduct, name='deleteproduct'),
    path('deleteproductadmin/<int:stid2>/', views.deleteproductadmin, name='deleteproductadmin'),
    path('addproductadmin/<int:stid2>/', views.addproductadmin, name='addproductadmin'),
    path('newcategory/', views.newcategory, name='newcategory'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
