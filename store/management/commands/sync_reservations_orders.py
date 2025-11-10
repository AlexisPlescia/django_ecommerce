from django.core.management.base import BaseCommand
from store.models import Reservation
from payment.models import Order as PaymentOrder
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Conecta reservas existentes con pedidos y crea pedidos para reservas confirmadas sin pedido'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== ANÁLISIS DE RESERVAS Y PEDIDOS ==='))
        
        # Analizar reservas existentes
        reservas = Reservation.objects.all()
        pedidos = PaymentOrder.objects.all()
        
        self.stdout.write(f'Total de reservas: {reservas.count()}')
        self.stdout.write(f'Total de pedidos: {pedidos.count()}')
        
        # Mostrar reservas confirmadas sin pedido
        reservas_confirmadas_sin_pedido = reservas.filter(
            status='confirmed', 
            converted_to_order=False
        )
        
        self.stdout.write(f'\nReservas confirmadas sin pedido: {reservas_confirmadas_sin_pedido.count()}')
        
        for reserva in reservas_confirmadas_sin_pedido:
            self.stdout.write(f'- Reserva #{reserva.id}: {reserva.customer_name} - {reserva.product.name} - ${reserva.total_price}')
        
        # Preguntar si crear pedidos automáticamente
        if reservas_confirmadas_sin_pedido.exists():
            confirm = input('\n¿Crear pedidos automáticamente para estas reservas? (s/N): ')
            if confirm.lower() in ['s', 'si', 'y', 'yes']:
                self.create_orders_from_reservations(reservas_confirmadas_sin_pedido)
        
        # Mostrar estado final
        self.stdout.write(self.style.SUCCESS('\n=== ESTADO FINAL ==='))
        reservas_convertidas = reservas.filter(converted_to_order=True)
        pedidos_con_reserva = pedidos.exclude(reservation=None)
        
        self.stdout.write(f'Reservas convertidas a pedidos: {reservas_convertidas.count()}')
        self.stdout.write(f'Pedidos vinculados a reservas: {pedidos_con_reserva.count()}')
    
    def create_orders_from_reservations(self, reservations):
        """Crea pedidos automáticamente desde las reservas"""
        created_count = 0
        
        for reserva in reservations:
            try:
                order = reserva.convert_to_order()
                if order:
                    created_count += 1
                    self.stdout.write(
                        f'✓ Creado pedido #{order.id} desde reserva #{reserva.id}'
                    )
                else:
                    self.stdout.write(
                        f'✗ No se pudo crear pedido para reserva #{reserva.id}'
                    )
            except Exception as e:
                self.stdout.write(
                    f'✗ Error al crear pedido para reserva #{reserva.id}: {e}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSe crearon {created_count} pedidos nuevos.')
        )
