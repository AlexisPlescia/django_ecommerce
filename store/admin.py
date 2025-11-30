from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile, Reservation, ProductImage, VisitCounter, VisitSummary
from django.contrib.auth.models import User

# Registro personalizado para Category con soporte de subcategorías
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'subcategory_count', 'product_count', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['parent__name', 'name']
    
    def subcategory_count(self, obj):
        """Muestra la cantidad de subcategorías"""
        return obj.subcategories.count()
    subcategory_count.short_description = 'Subcategorías'
    
    def product_count(self, obj):
        """Muestra la cantidad de productos en esta categoría"""
        return obj.get_all_products().count()
    product_count.short_description = 'Productos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent').prefetch_related('subcategories')

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)

# Inline para imágenes del producto
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'is_primary', 'order']

# Registro personalizado para Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'stock', 'is_available', 'is_sale']
    list_filter = ['category', 'is_available', 'is_sale']
    search_fields = ['name', 'description']
    list_editable = ['stock', 'is_available', 'is_sale']
    inlines = [ProductImageInline]

# Registro para ProductImage
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_primary', 'order']
    list_filter = ['is_primary', 'product']
    search_fields = ['product__name', 'alt_text']

# Registro personalizado para Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer_name', 'quantity', 'status', 'converted_to_order', 'created_at', 'customer_notified']
    list_filter = ['status', 'converted_to_order', 'created_at', 'customer_notified', 'admin_notified']
    search_fields = ['customer_name', 'customer_email', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'converted_to_order']
    list_editable = ['status']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('product', 'quantity', 'total_price')
        }),
        ('Información del Cliente', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Dirección de Envío', {
            'fields': ('shipping_address',)
        }),
        ('Estado de la Reserva', {
            'fields': ('status', 'expires_at', 'converted_to_order')
        }),
        ('Notificaciones', {
            'fields': ('customer_notified', 'admin_notified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Hace converted_to_order solo lectura después de la creación"""
        if obj and obj.converted_to_order:
            return self.readonly_fields + ['status']
        return self.readonly_fields


# Mix profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old way
admin.site.unregister(User)

# Re-Register the new way
admin.site.register(User, UserAdmin)

# Registro para VisitCounter
@admin.register(VisitCounter)
class VisitCounterAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'ip_address', 'page_url', 'browser', 'operating_system', 'is_mobile']
    list_filter = ['timestamp', 'is_mobile', 'browser', 'operating_system']
    search_fields = ['ip_address', 'user__username', 'page_url']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # No permitir agregar manualmente, solo por middleware
        return False

# Registro para VisitSummary
@admin.register(VisitSummary)
class VisitSummaryAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_visits', 'unique_visitors', 'logged_users_visits', 'anonymous_visits', 'mobile_visits', 'desktop_visits']
    list_filter = ['date']
    search_fields = ['date']
    readonly_fields = ['date', 'total_visits', 'unique_visitors', 'logged_users_visits', 'anonymous_visits', 'mobile_visits', 'desktop_visits']
    
    def has_add_permission(self, request):
        # No permitir agregar manualmente, se genera automáticamente
        return False
