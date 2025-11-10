from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem, ShippingMethod
from django.contrib.auth.models import User


# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)

# Administrador para métodos de envío
@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_cost', 'cost_per_kg', 'free_shipping_threshold', 'estimated_days', 'is_active')
    list_filter = ('is_active', 'name')
    search_fields = ('name',)
    list_editable = ('base_cost', 'cost_per_kg', 'free_shipping_threshold', 'is_active')

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0

# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
	model = Order
	readonly_fields = ["date_ordered"]
	fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "shipping_method", "shipping_cost", "total_with_shipping", "reservation", "date_ordered", "shipped", "date_shipped"]
	list_display = ["id", "full_name", "amount_paid", "shipping_cost", "total_with_shipping", "shipping_method", "reservation", "shipped", "date_ordered"]
	list_filter = ["shipped", "date_ordered"]
	search_fields = ["full_name", "email"]
	inlines = [OrderItemInline]

# Register our Order AND OrderAdmin
admin.site.register(Order, OrderAdmin)