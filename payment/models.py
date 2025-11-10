from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 
import datetime

class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255)
	shipping_email = models.CharField(max_length=255)
	shipping_address1 = models.CharField(max_length=255)
	shipping_city = models.CharField(max_length=255)
	shipping_state = models.CharField(max_length=255, null=True, blank=True)
	shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)


	# Don't pluralize address
	class Meta:
		verbose_name = "Dirección de Envío"
		verbose_name_plural = "Direcciones de Envío"

	def __str__(self):
		return f'Shipping Address - {str(self.id)}'

# Create a user Shipping Address by default when user signs up
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

# Automate the profile thing
post_save.connect(create_shipping, sender=User)



# Create Order Model
class Order(models.Model):
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250)
	email = models.EmailField(max_length=250)
	shipping_address = models.TextField(max_length=15000)
	amount_paid = models.DecimalField(max_digits=10, decimal_places=4)
	date_ordered = models.DateTimeField(auto_now_add=True)	
	shipped = models.BooleanField(default=False)
	date_shipped = models.DateTimeField(blank=True, null=True)
	
	# Campos de envío
	shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Método de Envío")
	shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo de Envío")
	total_with_shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total con Envío")
	
	# Relación con reservas (nuevo campo)
	reservation = models.ForeignKey('store.Reservation', on_delete=models.SET_NULL, null=True, blank=True, 
	                               help_text="Reserva que originó este pedido")
	
	def __str__(self):
		return f'Pedido #{self.id} - {self.full_name}'

	class Meta:
		verbose_name = "Pedido"
		verbose_name_plural = "Pedidos"

# Auto Add shipping Date
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
	if instance.pk:
		now = datetime.datetime.now()
		obj = sender._default_manager.get(pk=instance.pk)
		if instance.shipped and not obj.shipped:
			instance.date_shipped = now







# Create Order Items Model
class OrderItem(models.Model):
	# Foreign Keys
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=4)


	def __str__(self):
		return f'Order Item - {str(self.id)}'

	class Meta:
		verbose_name = "Artículo del Pedido"
		verbose_name_plural = "Artículos del Pedido"

# Modelo para manejar costos de envío
class ShippingMethod(models.Model):
    SHIPPING_CHOICES = [
        ('oca', 'OCA'),
        ('andreani', 'Andreani'),
        ('correo_argentino', 'Correo Argentino'),
    ]
    
    name = models.CharField(max_length=50, choices=SHIPPING_CHOICES, unique=True, verbose_name="Método de Envío")
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo Base")
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Costo por KG")
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Envío gratis desde")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    estimated_days = models.CharField(max_length=50, verbose_name="Días estimados", help_text="Ej: 3-5 días hábiles")
    
    class Meta:
        verbose_name = "Método de Envío"
        verbose_name_plural = "Métodos de Envío"
    
    def __str__(self):
        return f"{self.get_name_display()} - ${self.base_cost}"
    
    def calculate_cost(self, order_total, weight_kg=1):
        """Calcula el costo de envío basado en el total de la orden y peso"""
        if self.free_shipping_threshold and order_total >= self.free_shipping_threshold:
            return 0
        return self.base_cost + (self.cost_per_kg * weight_kg)