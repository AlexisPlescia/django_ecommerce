#!/usr/bin/env python
"""
Script para probar el envío gratuito con el nuevo umbral de $200,000
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.models import ShippingMethod
from payment.forms import ShippingMethodForm

def test_free_shipping():
    """Probar que el envío sea gratuito con compras de $200,000 o más"""
    
    test_amounts = [150000, 200000, 250000, 300000]
    
    print("🧪 PROBANDO ENVÍO GRATUITO CON NUEVO UMBRAL")
    print("=" * 60)
    
    for amount in test_amounts:
        print(f"\n💰 Probando con carrito de ${amount:,.0f}")
        print("-" * 40)
        
        for method in ShippingMethod.objects.filter(is_active=True):
            cost = method.calculate_cost(amount)
            
            if cost == 0:
                print(f"✅ {method.get_name_display()}: GRATIS 🎉")
            else:
                print(f"❌ {method.get_name_display()}: ${cost:,.0f}")
    
    print("\n" + "=" * 60)
    print("🎯 RESUMEN:")
    print("- Envío GRATUITO para compras ≥ $200,000")
    print("- Envío CON COSTO para compras < $200,000")

if __name__ == '__main__':
    test_free_shipping()
