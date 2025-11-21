#!/usr/bin/env python3
"""
Script para verificar y arreglar los métodos de envío
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.models import ShippingMethod
from payment.forms import ShippingMethodForm

def check_and_fix_shipping():
    print("🔧 VERIFICANDO MÉTODOS DE ENVÍO")
    print("=" * 50)
    
    # Verificar métodos existentes
    methods = ShippingMethod.objects.all()
    print(f"📊 Métodos en DB: {methods.count()}")
    
    for method in methods:
        print(f"   ID: {method.id}")
        print(f"   Nombre: {method.name} ({method.get_name_display()})")
        print(f"   Costo base: ${method.base_cost}")
        print(f"   Costo por kg: ${method.cost_per_kg}")
        print(f"   Envío gratis desde: ${method.free_shipping_threshold or 'N/A'}")
        print(f"   Días estimados: {method.estimated_days}")
        print(f"   Activo: {method.is_active}")
        print()
    
    print("=" * 50)
    print("🧪 PROBANDO FORMULARIO")
    
    # Probar formulario
    form = ShippingMethodForm(cart_total=28999)
    print("Choices del formulario:")
    for choice in form.fields['shipping_method'].choices:
        print(f"   {choice}")
    
    print("\n📝 HTML generado:")
    print(form['shipping_method'])
    
    return methods.count() > 0

if __name__ == '__main__':
    check_and_fix_shipping()
