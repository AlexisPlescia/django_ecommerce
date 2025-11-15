from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
from django.http import HttpResponseRedirect
import mercadopago
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from datetime import datetime, timedelta
from django.core.paginator import Paginator

def search(request):
    query = request.GET.get('q', '').strip()
    # Redirigir si la búsqueda coincide exactamente con una categoría (ignorando mayúsculas y espacios)
    category = Category.objects.filter(name__iexact=query).first()
    if category:
        # Normalizar el nombre para la URL
        url_name = category.name.replace(' ', '-')
        return redirect(f'/category/{url_name}')
    products = Product.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'search.html', context)

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def category_summary(request):
	categories = Category.objects.filter(parent=None)  # Solo categorías principales
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name__iexact=foo)
		products = category.get_all_products()  # Usar el nuevo método
		
		# Obtener subcategorías si es una categoría principal
		subcategories = category.subcategories.filter(is_active=True) if category.is_parent else None
		
		# Verificar si es la categoría "Armas" que requiere verificación de edad
		category_name_lower = category.name.lower()
		
		if category_name_lower in ['armas', 'arma', 'firearms', 'weapons']:
			return render(request, 'age_verification.html', {
				'products': products, 
				'category': category,
				'subcategories': subcategories
			})
		
		return render(request, 'category.html', {
			'products': products, 
			'category': category,
			'subcategories': subcategories
		})
	except Category.DoesNotExist:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')

def subcategory(request, parent_slug, subcategory_slug):
	"""Vista para subcategorías específicas"""
	parent_name = parent_slug.replace('-', ' ')
	subcategory_name = subcategory_slug.replace('-', ' ')
	
	try:
		parent_category = Category.objects.get(name__iexact=parent_name, parent=None)
		subcategory = Category.objects.get(name__iexact=subcategory_name, parent=parent_category)
		products = Product.objects.filter(category=subcategory)
		
		return render(request, 'subcategory.html', {
			'products': products,
			'subcategory': subcategory,
			'parent_category': parent_category
		})
	except Category.DoesNotExist:
		messages.error(request, "La subcategoría solicitada no existe.")
		return redirect('home')

def categories_ajax(request):
	"""Vista AJAX para obtener categorías en formato JSON"""
	categories_data = []
	for category in Category.objects.filter(parent=None, is_active=True):
		subcategories = []
		for sub in category.subcategories.filter(is_active=True):
			subcategories.append({
				'id': sub.id,
				'name': sub.name,
				'product_count': Product.objects.filter(category=sub).count()
			})
		
		categories_data.append({
			'id': category.id,
			'name': category.name,
			'product_count': category.get_all_products().count(),
			'subcategories': subcategories
		})
	
	return JsonResponse({'categories': categories_data})

def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})	

def login_user(request):
	if request.method == "POST":
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		
		# Validar que se proporcionaron credenciales
		if not email or not password:
			messages.error(request, "Por favor ingresa correo electrónico y contraseña.")
			return render(request, 'login.html', {})
		
		# Buscar usuarios activos por email
		try:
			users_with_email = User.objects.filter(email=email, is_active=True)
			
			if not users_with_email.exists():
				messages.error(request, "No existe una cuenta activa con este correo electrónico.")
				return render(request, 'login.html', {})
			
			# Intentar autenticar con cada usuario que tenga ese email
			authenticated_user = None
			for user_obj in users_with_email:
				test_user = authenticate(request, username=user_obj.username, password=password)
				if test_user is not None:
					authenticated_user = test_user
					break
			
			if authenticated_user is None:
				messages.error(request, "Correo electrónico o contraseña incorrectos. Intenta de nuevo.")
				return render(request, 'login.html', {})
			
			# Login exitoso
			login(request, authenticated_user)

			# Crear perfil si no existe
			try:
				current_user = Profile.objects.get(user__id=request.user.id)
			except Profile.DoesNotExist:
				current_user = Profile.objects.create(user=request.user)
			
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				try:
					# Convert to dictionary using JSON
					converted_cart = json.loads(saved_cart)
					# Add the loaded cart dictionary to our session
					# Get the cart
					cart = Cart(request)
					# Loop thru the cart and add the items from the database
					for key,value in converted_cart.items():
						cart.db_add(product=key, quantity=value)
				except json.JSONDecodeError:
					# Si hay error en el JSON, continuar sin carrito guardado
					pass

			messages.success(request, f"¡Bienvenido {authenticated_user.username}! Has iniciado sesión correctamente.")
			return redirect('home')
			
		except Exception as e:
			messages.error(request, "Error al procesar el login. Intenta de nuevo.")
			return render(request, 'login.html', {})

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Please Fill Out Your User Info Below..."))
			return redirect('update_info')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})

def pagar_producto(request, pk):
    product = Product.objects.get(id=pk)
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    # Si el precio es 0, no permitir pagar
    precio = float(product.sale_price if product.is_sale else product.price)
    if precio <= 0:
        from django.contrib import messages
        messages.error(request, "El precio del producto debe ser mayor a 0 para poder pagar.")
        return redirect('product', pk=pk)
    payer_email = request.user.email if request.user.is_authenticated and request.user.email else None
    # Guardar la orden antes de redirigir a Mercado Pago
    if request.user.is_authenticated:
        from .models import Order, Profile, Customer
        try:
            profile = Profile.objects.get(user__id=request.user)
        except Profile.DoesNotExist:
            profile = None
        # Buscar o crear el Customer asociado al usuario
        customer, _ = Customer.objects.get_or_create(
            email=request.user.email,
            defaults={
                'first_name': request.user.first_name or 'Nombre',
                'last_name': request.user.last_name or 'Apellido',
                'phone': profile.phone if profile else '',
                'password': 'unused',
            }
        )
        orden_existente = Order.objects.filter(product=product, customer=customer, address=profile.address1 if profile else '', phone=profile.phone if profile else '', status=False).first()
        if not orden_existente:
            Order.objects.create(
                product=product,
                customer=customer,
                quantity=1,
                address=profile.address1 if profile else '',
                phone=profile.phone if profile else '',
                status=False  # Pendiente de pago
            )
        # Para debug/test
        print(f'Orden creada para producto {product.id} y usuario {request.user.id}')
    # Construir back_urls
    host = request.get_host()
    scheme = 'https' if request.is_secure() else 'http'
    back_urls = {
        "success": f"{scheme}://{host}/payment/payment_success",
        "failure": f"{scheme}://{host}/payment/payment_failed",
        "pending": f"{scheme}://{host}/payment/payment_failed"
    }
    notification_url = f"{scheme}://{host}/store/webhook/mercadopago/"
    preference_data = {
        "items": [
            {
                "title": product.name or "Producto sin nombre",
                "quantity": 1,
                "unit_price": precio,
                "description": product.description or "Compra desde el ecommerce",
                "currency_id": "ARS",
            }
        ],
        "back_urls": back_urls,
        "auto_return": "approved",
        "notification_url": notification_url,
    }
    if payer_email:
        preference_data["payer"] = {"email": payer_email}
    preference_response = sdk.preference().create(preference_data)
    print("MercadoPago preference response:", preference_response)  # LOG para depuración
    if "response" in preference_response and "init_point" in preference_response["response"]:
        return HttpResponseRedirect(preference_response["response"]["init_point"])
    else:
        from django.contrib import messages
        error_msg = preference_response.get("message", "No se pudo crear la preferencia de pago. Intente nuevamente.")
        messages.error(request, f"Error Mercado Pago: {error_msg}")
        return redirect('product', pk=pk)

@csrf_exempt
def mercadopago_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        payment_id = data.get('data', {}).get('id') or data.get('id')
        topic = data.get('type') or data.get('topic')
        if topic == 'payment' and payment_id:
            import mercadopago
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(payment_id)
            status = payment_info['response'].get('status')
            payer_email = payment_info['response'].get('payer', {}).get('email')
            # Buscar la orden asociada a este payment_id
            from .models import Order
            ordenes = Order.objects.filter(payment_id=payment_id)
            if status == 'approved' and payer_email and ordenes.exists():
                # Armar detalle de la compra
                detalle_items = ""
                total = 0
                for orden in ordenes:
                    prod = orden.product
                    cantidad = orden.quantity
                    precio_unit = prod.sale_price if prod.is_sale else prod.price
                    subtotal = precio_unit * cantidad
                    total += subtotal
                    detalle_items += f"{cantidad} x {prod.name} por ${precio_unit} cada uno.\n"
                # Email al cliente
                cliente_subject = "Confirmación de tu compra en MiMarca"
                cliente_message = f"""
Estás recibiendo este e-mail porque comenzaste una compra en MiMarca.\n\nTe enviaremos el pedido cuando recibamos la confirmación de la venta por parte del medio de pago. La confirmación puede demorar hasta 24hs.\n\nNúmero de orden: #{ordenes.first().id}\n\nTu orden incluye:\n{detalle_items}\nTotal: ${total}\n\nSi no realizaste esta compra o simplemente estabas probando nuestro sitio, por favor desconsidera este e-mail.\n\nAtentamente,\nMiMarca"""
                send_mail(
                    cliente_subject,
                    cliente_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [payer_email],
                    fail_silently=True,
                )
                # Email al vendedor
                vendedor_subject = f"Nueva compra realizada - Orden #{ordenes.first().id}"
                vendedor_message = f"Se ha realizado una nueva compra en MiMarca.\n\nNúmero de orden: #{ordenes.first().id}\nCliente: {payer_email}\nDetalle:\n{detalle_items}\nTotal: ${total}\n"
                send_mail(
                    vendedor_subject,
                    vendedor_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ["alexisplescia123@gmail.com"],
                    fail_silently=True,
                )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'only POST allowed'})


def is_superuser(user):
    """Verificar si el usuario es superusuario"""
    return user.is_superuser

@user_passes_test(is_superuser)
def visit_stats(request):
    """Vista de estadísticas de visitas - Solo para superusuarios"""
    from .models import VisitCounter, VisitSummary
    
    # Estadísticas generales
    total_visits = VisitCounter.objects.count()
    
    # Visitas de los últimos 7 días
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_visits = VisitCounter.objects.filter(timestamp__gte=seven_days_ago).count()
    
    # Visitantes únicos (por IP)
    unique_visitors = VisitCounter.objects.values('ip_address').distinct().count()
    
    # Visitas por día (últimos 30 días)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    daily_stats = VisitSummary.objects.filter(
        date__gte=thirty_days_ago.date()
    ).order_by('-date')[:30]
    
    # Páginas más visitadas
    popular_pages = VisitCounter.objects.values('page_url').annotate(
        visit_count=Count('page_url')
    ).order_by('-visit_count')[:10]
    
    # Navegadores más usados
    browsers = VisitCounter.objects.values('browser').annotate(
        count=Count('browser')
    ).order_by('-count')[:5]
    
    # Sistemas operativos
    operating_systems = VisitCounter.objects.values('operating_system').annotate(
        count=Count('operating_system')
    ).order_by('-count')[:5]
    
    # Dispositivos móviles vs desktop
    mobile_visits = VisitCounter.objects.filter(is_mobile=True).count()
    desktop_visits = VisitCounter.objects.filter(is_mobile=False).count()
    
    # Visitas de usuarios registrados vs anónimos
    logged_visits = VisitCounter.objects.filter(user__isnull=False).count()
    anonymous_visits = VisitCounter.objects.filter(user__isnull=True).count()
    
    # Últimas visitas (paginadas)
    recent_visits_list = VisitCounter.objects.select_related('user').order_by('-timestamp')
    paginator = Paginator(recent_visits_list, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'total_visits': total_visits,
        'recent_visits': recent_visits,
        'unique_visitors': unique_visitors,
        'daily_stats': daily_stats,
        'popular_pages': popular_pages,
        'browsers': browsers,
        'operating_systems': operating_systems,
        'mobile_visits': mobile_visits,
        'desktop_visits': desktop_visits,
        'logged_visits': logged_visits,
        'anonymous_visits': anonymous_visits,
        'page_obj': page_obj,
    }
    
    return render(request, 'admin/visit_stats.html', context)