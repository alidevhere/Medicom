from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from online_pharmacy.admin import admin_site



urlpatterns = [

    path('', views.get_search, name='home_page'),
    path('request_product/', views.request_product, name='request_product'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout, name= 'logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('store_page/', views.store_page, name='store_page'),
    path('update_item/', views.updateItem, name='update_item'),
    path('user_panel/my_orders/', views.my_orders,name='my_orders'),
    path('user_panel/track_my_orders/', views.track_my_orders, name='track_my_orders'),
    path('user_panel/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('user_panel/view_profile/', views.view_profile, name='view_profile'),
    path('user_panel/track_my_orders/<int:order_id>', views.customer_pnl_view_details, name='view_order_details'),
    path('user_panel/my_orders/<int:order_id>', views.customer_pnl_view_orders_details, name='view_complete_order_details'),
    path('view_details/<int:p_id>/', views.view_details, name='view_details'),
    path('admin/', admin_site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)