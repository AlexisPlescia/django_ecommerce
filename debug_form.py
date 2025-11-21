#!/usr/bin/env python3
"""
Script para debuggear el ShippingMethodForm
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.forms import ShippingMethodForm
from payment.models import ShippingMethod

def debug_shipping_form():
    print("🔍 DEBUGGING SHIPPING METHOD FORM")
    print("=" * 50)
    
    # Verificar métodos en DB
    methods = ShippingMethod.objects.filter(is_active=True)
    print(f"📊 Métodos de envío en DB: {methods.count()}")
    for method in methods:
        print(f"   - {method.name} ({method.get_name_display()}) - ${method.base_cost}")
    
    print("\n" + "=" * 50)
    
    # Crear formulario
    form = ShippingMethodForm(cart_total=10000)
    
    print("📝 HTML DEL FORMULARIO:")
    print("-" * 30)
    print(form.as_p())
    
    print("\n📋 CAMPO SHIPPING_METHOD:")
    print("-" * 30)
    print(f"Widget: {type(form.fields['shipping_method'].widget)}")
    print(f"Choices: {form.fields['shipping_method'].choices}")
    
    print("\n🔧 HTML ESPECÍFICO DEL FIELD:")
    print("-" * 30)
    print(form['shipping_method'])

if __name__ == '__main__':
    debug_shipping_form()
