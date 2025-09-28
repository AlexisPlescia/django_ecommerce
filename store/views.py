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

def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	


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
	categories = Category.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


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
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			# Do some shopping cart stuff
			current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
			saved_cart = current_user.old_cart
			# Convert database string to python dictionary
			if saved_cart:
				# Convert to dictionary using JSON
				converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
				cart = Cart(request)
				# Loop thru the cart and add the items from the database
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)

			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

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
            profile = Profile.objects.get(user=request.user)
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