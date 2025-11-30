from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create Customer Profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_modified = models.DateTimeField(User, auto_now=True)
	phone = models.CharField(max_length=20, blank=True)
	address1 = models.CharField(max_length=200, blank=True)
	address2 = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	state = models.CharField(max_length=200, blank=True)
	zipcode = models.CharField(max_length=200, blank=True)
	country = models.CharField(max_length=200, blank=True)
	old_cart = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = "Perfil"
		verbose_name_plural = "Perfiles"

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)







# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
	description = models.TextField(blank=True, null=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		if self.parent:
			return f"{self.parent.name} > {self.name}"
		return self.name

	def get_all_products(self):
		"""Obtiene todos los productos de esta categoría y sus subcategorías"""
		from django.db.models import Q
		if self.subcategories.exists():
			# Si tiene subcategorías, incluir productos de todas las subcategorías
			subcategory_ids = [sub.id for sub in self.subcategories.all()]
			return Product.objects.filter(Q(category=self) | Q(category__id__in=subcategory_ids))
		else:
			# Si no tiene subcategorías, solo productos de esta categoría
			return Product.objects.filter(category=self)

	@property
	def is_parent(self):
		return self.parent is None

	@property
	def is_subcategory(self):
		return self.parent is not None
	
	def get_slug(self):
		"""Genera un slug único para esta categoría"""
		from django.utils.text import slugify
		return slugify(self.name)
	
	def get_url_slug(self):
		"""Obtiene el slug para usar en URLs"""
		return self.get_slug()
	
	def save(self, *args, **kwargs):
		"""Override save para validaciones adicionales"""
		# Validar que no haya duplicados
		if self.parent:
			# Para subcategorías, verificar duplicados dentro del mismo padre
			existing = Category.objects.filter(
				name__iexact=self.name, 
				parent=self.parent
			).exclude(id=self.id)
			if existing.exists():
				raise ValueError(f"Ya existe una subcategoría '{self.name}' en '{self.parent.name}'")
		else:
			# Para categorías principales, verificar duplicados globales
			existing = Category.objects.filter(
				name__iexact=self.name, 
				parent=None
			).exclude(id=self.id)
			if existing.exists():
				raise ValueError(f"Ya existe una categoría principal '{self.name}'")
		
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = "Categoría"
		verbose_name_plural = "Categorías"


# Modelo para imágenes adicionales del producto
class ProductImage(models.Model):
	product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='additional_images')
	image = models.ImageField(upload_to='uploads/product/gallery/')
	alt_text = models.CharField(max_length=200, blank=True, null=True)
	is_primary = models.BooleanField(default=False)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ['order', 'id']
		verbose_name = "Imagen de Producto"
		verbose_name_plural = "Imágenes de Productos"

	def __str__(self):
		return f"{self.product.name} - Imagen {self.order}"

	def save(self, *args, **kwargs):
		# Si es marcada como primaria, desmarcar las otras
		if self.is_primary:
			ProductImage.objects.filter(product=self.product, is_primary=True).exclude(id=self.id).update(is_primary=False)
		super().save(*args, **kwargs)


# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)


	def __str__(self):
		return f'{self.first_name} {self.last_name}'

	class Meta:
		verbose_name = "Cliente"
		verbose_name_plural = "Clientes"



# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(decimal_places=2, default=0, help_text='Precio en pesos argentinos (ARS)', max_digits=12)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=250, default='', blank=True, null=True)
	image = models.ImageField(blank=True, null=True, upload_to='uploads/product/')
	# Add Sale Stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(decimal_places=2, default=0, help_text='Precio de oferta en pesos argentinos (ARS)', max_digits=12)
	# Add Stock Management
	stock = models.PositiveIntegerField(default=0, help_text="Cantidad disponible en inventario")
	is_available = models.BooleanField(default=True, help_text="Disponible para compra")

	def __str__(self):
		return self.name

	@property
	def is_in_stock(self):
		"""Verifica si el producto tiene stock disponible"""
		try:
			return self.stock > 0 and self.is_available
		except AttributeError:
			# Si los campos no existen, asumir que está disponible
			return True
	
	def reduce_stock(self, quantity):
		"""Reduce el stock del producto y actualiza disponibilidad"""
		if self.stock >= quantity:
			self.stock -= quantity
			if self.stock == 0:
				self.is_available = False
			self.save()
			return True
		return False

	def get_all_images(self):
		"""Obtiene todas las imágenes del producto (principal + adicionales)"""
		images = []
		# Imagen principal
		if self.image:
			images.append({
				'url': self.image.url,
				'alt_text': f"{self.name} - Imagen principal",
				'is_primary': True
			})
		
		# Imágenes adicionales
		for img in self.additional_images.all():
			images.append({
				'url': img.image.url,
				'alt_text': img.alt_text or f"{self.name} - Imagen {img.order}",
				'is_primary': img.is_primary
			})
		
		return images

	def get_primary_image(self):
		"""Obtiene la imagen principal del producto"""
		# Buscar imagen marcada como primaria en las adicionales
		primary_additional = self.additional_images.filter(is_primary=True).first()
		if primary_additional:
			return primary_additional.image.url
		
		# Si no hay imagen primaria adicional, usar la imagen del modelo principal
		if self.image:
			return self.image.url
		
		return None

	class Meta:
		verbose_name = "Producto"
		verbose_name_plural = "Productos"


# Customer Orders
class Order(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.CharField(max_length=100, default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)
	payment_id = models.CharField(max_length=100, blank=True, null=True, help_text="ID de pago de Mercado Pago")

	def __str__(self):
		return self.product

	class Meta:
		verbose_name = "Orden"
		verbose_name_plural = "Órdenes"


# Product Reservations
class Reservation(models.Model):
	RESERVATION_STATUS = [
		('pending', 'Pendiente'),
		('confirmed', 'Confirmada'),
		('cancelled', 'Cancelada'),
		('expired', 'Expirada'),
	]
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	
	# Customer information (for guests or additional info)
	customer_name = models.CharField(max_length=100)
	customer_email = models.EmailField()
	customer_phone = models.CharField(max_length=20, blank=True, null=True)
	
	# Shipping information
	shipping_address = models.TextField()
	
	# Reservation details
	total_price = models.DecimalField(max_digits=10, decimal_places=4)
	status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='pending')
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	expires_at = models.DateTimeField(null=True, blank=True, help_text="Fecha de expiración de la reserva")
	
	# Email notifications
	customer_notified = models.BooleanField(default=False)
	admin_notified = models.BooleanField(default=False)
	
	# Estado de conversión a pedido
	converted_to_order = models.BooleanField(default=False, help_text="Indica si esta reserva se convirtió en un pedido pagado")
	
	class Meta:
		ordering = ['-created_at']
		verbose_name = "Reserva"
		verbose_name_plural = "Reservas"
	
	def __str__(self):
		return f"Reserva #{self.id} - {self.product.name} ({self.quantity})"
	
	def confirm_reservation(self):
		"""Confirma la reserva y actualiza el stock"""
		if self.status == 'pending':
			success = self.product.reduce_stock(self.quantity)
			if success:
				self.status = 'confirmed'
				self.save()
				return True
		return False
	
	def cancel_reservation(self):
		"""Cancela la reserva y restaura el stock si fue confirmada"""
		if self.status == 'confirmed':
			self.product.stock += self.quantity
			if not self.product.is_available and self.product.stock > 0:
				self.product.is_available = True
			self.product.save()
		
		self.status = 'cancelled'
		self.save()
	
	def convert_to_order(self):
		"""Convierte la reserva en un pedido de payment.Order"""
		if self.status != 'confirmed':
			return None
		
		if self.converted_to_order:
			return None  # Ya fue convertida
		
		# Importar aquí para evitar importación circular
		from payment.models import Order as PaymentOrder
		
		# Crear el pedido
		order = PaymentOrder.objects.create(
			user=self.user,
			full_name=self.customer_name,
			email=self.customer_email,
			shipping_address=self.shipping_address,
			amount_paid=self.total_price,
			reservation=self
		)
		
		# Marcar como convertida
		self.converted_to_order = True
		self.save()
		
		return order

# Modelos para contador de visitas
class VisitCounter(models.Model):
    """Modelo para contar visitas al sitio"""
    
    # Información básica de la visita
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    
    # Usuario (si está logueado)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Información de la página visitada
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    # Información del dispositivo/navegador
    is_mobile = models.BooleanField(default=False)
    browser = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    
    # Información geográfica (opcional)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
    
    def __str__(self):
        user_info = f"Usuario: {self.user.username}" if self.user else f"IP: {self.ip_address}"
        return f"{user_info} - {self.page_url} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

class VisitSummary(models.Model):
    """Resumen diario de visitas para mejor rendimiento"""
    
    date = models.DateField(unique=True)
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    logged_users_visits = models.PositiveIntegerField(default=0)
    anonymous_visits = models.PositiveIntegerField(default=0)
    mobile_visits = models.PositiveIntegerField(default=0)
    desktop_visits = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Resumen de Visitas"
        verbose_name_plural = "Resúmenes de Visitas"
    
    def __str__(self):
        return f"Visitas del {self.date.strftime('%d/%m/%Y')}: {self.total_visits} total"