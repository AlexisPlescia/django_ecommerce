#!/usr/bin/env python
"""
Script para debuggear el checkout
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

def debug_checkout():
    """Verificar la configuración del checkout"""
    
    print("🔍 DEBUGGING CHECKOUT:")
    print("=" * 50)
    
    # 1. Verificar métodos de envío
    print("\n1. 📦 MÉTODOS DE ENVÍO EN BASE DE DATOS:")
    methods = ShippingMethod.objects.filter(is_active=True)
    for method in methods:
        print(f"   - {method.get_name_display()} (${method.base_cost}) - {method.estimated_days}")
    
    # 2. Verificar formulario
    print(f"\n2. 📋 TOTAL DE MÉTODOS ACTIVOS: {methods.count()}")
    
    if methods.count() > 0:
        print("\n3. 🎯 FORMULARIO DE ENVÍO:")
        form = ShippingMethodForm(cart_total=10000)
        print("   Widget del campo:", type(form.fields['shipping_method'].widget).__name__)
        print("   Choices del formulario:")
        for choice in form.fields['shipping_method'].choices:
            print(f"     - {choice}")
    else:
        print("\n❌ NO HAY MÉTODOS DE ENVÍO ACTIVOS")
    
    print("\n" + "=" * 50)
    print("✅ Debug completado")

if __name__ == '__main__':
    debug_checkout()
