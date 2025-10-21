from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from cart.cart import Cart
from store.models import Product, Profile, Reservation
from payment.models import ShippingAddress
import datetime
from datetime import timedelta


def create_reservation(request):
    """
    Crea una reserva desde el carrito de compras
    """
    if request.method == 'POST':
        # Obtener el carrito
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        
        # Obtener información de envío de la sesión
        my_shipping = request.session.get('my_shipping')
        if not my_shipping:
            messages.error(request, "No se encontró información de envío. Por favor complete el checkout nuevamente.")
            return redirect('checkout')
        
        # Validar stock para todos los productos
        stock_errors = []
        for product in cart_products:
            quantity = quantities().get(str(product.id), 0)
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
                quantity = quantities().get(str(product.id), 0)
                
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
                    expires_at=datetime.datetime.now() + timedelta(hours=24)  # Expira en 24 horas
                )
                
                # Confirmar la reserva (esto reduce el stock)
                if reservation.confirm_reservation():
                    reservations_created.append(reservation)
                else:
                    # Si falla, eliminar la reserva
                    reservation.delete()
                    messages.error(request, f"Error al reservar {product.name}")
                    return redirect('cart_summary')
            
            # Si llegamos aquí, todas las reservas fueron exitosas
            # Enviar correos de notificación
            send_reservation_emails(reservations_created, my_shipping)
            
            # Limpiar el carrito
            clear_cart(request)
            
            # Mensaje de éxito
            messages.success(request, f"¡Reserva confirmada! Se crearon {len(reservations_created)} reservas exitosamente. Recibirás un correo de confirmación.")
            
            # Redirigir a página de éxito
            return render(request, 'payment/reservation_success.html', {
                'reservations': reservations_created,
                'total_reservations': len(reservations_created)
            })
            
        except Exception as e:
            # Si algo falla, cancelar todas las reservas creadas
            for reservation in reservations_created:
                reservation.cancel_reservation()
                reservation.delete()
            
            messages.error(request, f"Error al procesar la reserva: {str(e)}")
            return redirect('cart_summary')
    
    else:
        return redirect('home')


def send_reservation_emails(reservations, shipping_info):
    """
    Envía correos de confirmación al cliente y notificación al admin
    """
    customer_email = shipping_info['shipping_email']
    customer_name = shipping_info['shipping_full_name']
    
    # Email al cliente
    try:
        subject_customer = 'Confirmación de Reserva - Tu pedido ha sido procesado'
        
        # Renderizar template HTML para el cliente
        html_content_customer = render_to_string('emails/reservation_confirmation.html', {
            'customer_name': customer_name,
            'reservations': reservations,
            'total_amount': sum(r.total_price for r in reservations),
            'shipping_address': reservations[0].shipping_address if reservations else '',
        })
        
        text_content_customer = strip_tags(html_content_customer)
        
        email_customer = EmailMultiAlternatives(
            subject_customer,
            text_content_customer,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )
        email_customer.attach_alternative(html_content_customer, "text/html")
        email_customer.send()
        
        # Marcar como notificado
        for reservation in reservations:
            reservation.customer_notified = True
            reservation.save()
            
    except Exception as e:
        print(f"Error enviando email al cliente: {e}")
    
    # Email al admin
    try:
        admin_emails = [settings.DEFAULT_FROM_EMAIL]  # Puedes configurar emails de admin
        subject_admin = f'Nueva Reserva Recibida - {len(reservations)} productos'
        
        html_content_admin = render_to_string('emails/reservation_admin.html', {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'reservations': reservations,
            'total_amount': sum(r.total_price for r in reservations),
            'shipping_address': reservations[0].shipping_address if reservations else '',
        })
        
        text_content_admin = strip_tags(html_content_admin)
        
        email_admin = EmailMultiAlternatives(
            subject_admin,
            text_content_admin,
            settings.DEFAULT_FROM_EMAIL,
            admin_emails
        )
        email_admin.attach_alternative(html_content_admin, "text/html")
        email_admin.send()
        
        # Marcar como notificado
        for reservation in reservations:
            reservation.admin_notified = True
            reservation.save()
            
    except Exception as e:
        print(f"Error enviando email al admin: {e}")


def clear_cart(request):
    """
    Limpia el carrito del usuario
    """
    # Limpiar sesión
    for key in list(request.session.keys()):
        if key == "session_key":
            del request.session[key]
    
    # Limpiar carrito en BD para usuarios autenticados
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.filter(user__id=request.user.id)
            current_user.update(old_cart="")
        except:
            pass


def reservation_detail(request, reservation_id):
    """
    Muestra los detalles de una reserva específica
    """
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


def my_reservations(request):
    """
    Muestra las reservas del usuario autenticado
    """
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para ver tus reservas.")
        return redirect('login')
    
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'payment/my_reservations.html', {
        'reservations': reservations
    })


def admin_reservations(request):
    """
    Vista para admin para ver todas las reservas
    """
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.error(request, "Acceso denegado.")
        return redirect('home')
    
    reservations = Reservation.objects.all().order_by('-created_at')
    
    return render(request, 'payment/admin_reservations.html', {
        'reservations': reservations
    })
