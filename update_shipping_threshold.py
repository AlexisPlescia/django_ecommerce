#!/usr/bin/env python
"""
Script para actualizar los umbrales de envío gratuito a $200,000
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.models import ShippingMethod

def update_shipping_thresholds():
    """Actualizar todos los métodos de envío para que tengan umbral de $200,000"""
    
    new_threshold = 200000.00
    
    print(f"🚀 Actualizando umbrales de envío gratuito a ${new_threshold:,.0f}")
    
    updated_count = 0
    for method in ShippingMethod.objects.all():
        old_threshold = method.free_shipping_threshold
        method.free_shipping_threshold = new_threshold
        method.save()
        
        print(f"✅ {method.get_name_display()}: ${old_threshold:,.0f} → ${new_threshold:,.0f}")
        updated_count += 1
    
    print(f"\n🎉 ¡{updated_count} métodos de envío actualizados exitosamente!")
    print(f"💰 Nuevo umbral para envío gratuito: ${new_threshold:,.0f}")

if __name__ == '__main__':
    print("🔄 Actualizando umbrales de envío gratuito...")
    update_shipping_thresholds()
    print("✅ ¡Actualización completada!")
