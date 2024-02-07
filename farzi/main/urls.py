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
    path('',views.index,name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('display_all_objects/', views.display_all_objects, name='display_all_objects'),
    path('singleview/<int:product_id>/',views.singleview,name='singleview'),
    path('inactiveseller/<int:stid2>/',views.inactiveseller, name='inactiveseller'),
    path('add_cart/<int:bookid2>/', views.add_cart, name='add_cart'),
    path('add_cart1/<int:bookid2>/', views.add_cart1, name='add_cart1'),
    path('delete_cart/<int:bookid2>/', views.delete_cart, name='delete_cart'),
    path('list/<str:category>/', views.book_list_by_category, name='book_list_by_category'),
    path('list/sub/<str:category>/', views.book_list_by_subcategory, name='book_list_by_subcategory'),
    path('search_product/',views.search_product,name='search_product'),
    path('list',views.list,name="list"), 
    path('cart',views.cart,name="cart"), 
    path('increase_item/<int:item_id>/', views.increase_item, name='increase_item'),
    path('decrease_item/<int:item_id>/', views.decrease_item, name='decrease_item'),
    path('wishlist',views.wishlist,name="wishlist"),
    path('add_wishlist/<int:bookid2>/', views.add_wishlist, name='add_wishlist'),
    path('delete_wishlist/<int:bookid2>/', views.delete_wishlist, name='delete_wishlist'),
    path('buyNowComplete/<int:product_id>/', views.buyNowComplete, name='buyNowComplete'),
    path('delete_wishlistpage/<int:bookid2>/', views.delete_wishlistpage, name='delete_wishlistpage'),
    path('separate/', views.separate, name='separate'),
    path('product-list/', views.product_list, name='product_list'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('paymentsuccess/', views.paymentsuccess, name='paymentsuccess'),
    path('paymentfail/', views.paymentfail, name='paymentfail'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('order1/', views.checkout_complete, name='order1'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('deletepending/', views.deletepending, name='deletepending'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('salesadmin/', views.salesadmin, name='salesadmin'),
    path('seminar/', views.seminar, name='seminar'),
    path('create_order/', views.create_order, name='create_order'),
    path('homepage/', views.homepage, name='homepage'),
    path('print_as_pdf/<int:stid2>/', views.print_as_pdf, name='print_as_pdf'),
    

    





    

]
