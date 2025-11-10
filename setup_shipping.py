#!/usr/bin/env python
"""
Script para configurar los métodos de envío iniciales
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/backup_sniper_octubre_21/Django-Ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.models import ShippingMethod

def setup_shipping_methods():
    """Crear métodos de envío si no existen"""
    
    shipping_methods = [
        {
            'name': 'oca',
            'base_cost': 2500.00,
            'cost_per_kg': 500.00,
            'free_shipping_threshold': 50000.00,
            'estimated_days': '3-5 días hábiles',
            'is_active': True
        },
        {
            'name': 'andreani',
            'base_cost': 3000.00,
            'cost_per_kg': 600.00,
            'free_shipping_threshold': 60000.00,
            'estimated_days': '2-4 días hábiles',
            'is_active': True
        },
        {
            'name': 'correo_argentino',
            'base_cost': 2000.00,
            'cost_per_kg': 400.00,
            'free_shipping_threshold': 45000.00,
            'estimated_days': '4-7 días hábiles',
            'is_active': True
        },
    ]
    
    for method_data in shipping_methods:
        method, created = ShippingMethod.objects.get_or_create(
            name=method_data['name'],
            defaults=method_data
        )
        
        if created:
            print(f"✅ Método de envío creado: {method.get_name_display()} - ${method.base_cost}")
        else:
            print(f"⚠️  Método de envío ya existe: {method.get_name_display()}")
    
    print(f"\n🚚 Total de métodos de envío configurados: {ShippingMethod.objects.count()}")

if __name__ == '__main__':
    print("🚀 Configurando métodos de envío...")
    setup_shipping_methods()
    print("✅ ¡Configuración completada!")
