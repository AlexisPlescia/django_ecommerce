from django.urls import path
from . import views

urlpatterns = [
	path('', views.cart_summary, name="cart_summary"),
	path('add/', views.cart_add, name="cart_add"),
	path('delete/', views.cart_delete, name="cart_delete"),
	path('update/', views.cart_update, name="cart_update"),
   # path("pago_exitoso", views.pago_exitoso, name="pago_exitoso"),
    #path("pago_fallido", views.pago_fallido, name="pago_fallido"),
   # path("pago_pendiente", views.pago_pendiente, name="pago_pendiente"),
]
