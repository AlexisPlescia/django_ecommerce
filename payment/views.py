from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
import mercadopago
from django.conf import settings

# Import Some Paypal Stuff
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
import uuid # unique user id for duplictate orders

# Se removieron los imports de reservas para evitar circular imports

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def process_order(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")


			messages.success(request, "Order Placed!")
			return redirect('home')

			

		else:
			# not logged in
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('home')


	else:
		messages.success(request, "Access Denied")
		return redirect('home')

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Importar modelos necesarios
        from store.models import Reservation
        from datetime import timedelta
        from django.core.mail import send_mail, EmailMultiAlternatives
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        
        # Validar stock para todos los productos
        stock_errors = []
        for product in cart_products:
            quantity = quantities.get(str(product.id), 0)
            if not product.is_in_stock:
                stock_errors.append(f"{product.name} no está disponible")
            elif product.stock < quantity:
                stock_errors.append(f"{product.name} solo tiene {product.stock} unidades disponibles")
        
        if stock_errors:
            for error in stock_errors:
                messages.error(request, error)
            return redirect('cart_summary')
        
        # Crear reservas para cada producto
        reservations_created = []
        try:
            for product in cart_products:
                quantity = quantities.get(str(product.id), 0)
                
                # Calcular precio
                if product.is_sale:
                    unit_price = product.sale_price
                else:
                    unit_price = product.price
                
                total_price = unit_price * quantity
                
                # Crear la reserva
                reservation = Reservation.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    product=product,
                    quantity=quantity,
                    customer_name=my_shipping['shipping_full_name'],
                    customer_email=my_shipping['shipping_email'],
                    customer_phone=my_shipping.get('shipping_phone', ''),
                    shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_city']}\n{my_shipping.get('shipping_state', '')}\n{my_shipping.get('shipping_zipcode', '')}",
                    total_price=total_price,
                    expires_at=datetime.datetime.now() + timedelta(hours=24)
                )
                
                # Confirmar la reserva (esto reduce el stock)
                if reservation.confirm_reservation():
                    reservations_created.append(reservation)
                else:
                    reservation.delete()
                    messages.error(request, f"Error al reservar {product.name}")
                    return redirect('cart_summary')
            
            # Limpiar el carrito
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            if request.user.is_authenticated:
                try:
                    current_user = Profile.objects.filter(user__id=request.user.id)
                    current_user.update(old_cart="")
                except:
                    pass
            
            # Mensaje de éxito
            messages.success(request, f"¡Reserva confirmada! Se crearon {len(reservations_created)} reservas exitosamente.")
            
            return render(request, 'payment/reservation_success.html', {
                'reservations': reservations_created,
                'total_reservations': len(reservations_created)
            })
            
        except Exception as e:
            # Si algo falla, cancelar todas las reservas creadas
            for reservation in reservations_created:
                try:
                    reservation.cancel_reservation()
                    reservation.delete()
                except:
                    pass
            
            messages.error(request, f"Error al procesar la reserva: {str(e)}")
            return redirect('cart_summary')
        
    else:
        messages.error(request, "Acceso denegado")
        return redirect('home')

def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

	

def payment_success(request):
	return render(request, "payment/payment_success.html", {})


def payment_failed(request):
	return render(request, "payment/payment_failed.html", {})


# Vistas de Reservas
def my_reservations(request):
    """
    Muestra las reservas del usuario autenticado
    """
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver tus reservas.")
        return redirect('login')
    
    from store.models import Reservation
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'payment/my_reservations.html', {
        'reservations': reservations
    })


def reservation_detail(request, reservation_id):
    """
    Muestra los detalles de una reserva específica
    """
    from store.models import Reservation
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        
        # Verificar que el usuario puede ver esta reserva
        if request.user.is_authenticated:
            if not (reservation.user == request.user or request.user.is_superuser):
                messages.error(request, "No tienes permiso para ver esta reserva.")
                return redirect('home')
        else:
            messages.error(request, "Debes iniciar sesión para ver los detalles de la reserva.")
            return redirect('login')
        
        return render(request, 'payment/reservation_detail.html', {
            'reservation': reservation
        })
        
    except Reservation.DoesNotExist:
        messages.error(request, "Reserva no encontrada.")
        return redirect('home')


def admin_reservations(request):
    """
    Vista para admin para ver todas las reservas
    """
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.error(request, "Acceso denegado.")
        return redirect('home')
    
    from store.models import Reservation
    reservations = Reservation.objects.all().order_by('-created_at')
    
    return render(request, 'payment/admin_reservations.html', {
        'reservations': reservations
    })