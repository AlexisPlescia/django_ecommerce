from django.urls import path, include
from . import views

urlpatterns = [
    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_info', views.billing_info, name="billing_info"),
    path('process_order', views.process_order, name="process_order"),
    path('shipped_dash', views.shipped_dash, name="shipped_dash"),
    path('not_shipped_dash', views.not_shipped_dash, name="not_shipped_dash"),
    path('orders/<int:pk>', views.orders, name='orders'),
    path('paypal', include("paypal.standard.ipn.urls")),

    # URLs para sistema de reservas
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('admin_reservations/', views.admin_reservations, name='admin_reservations'),
]
