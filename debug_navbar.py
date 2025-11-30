#!/usr/bin/env python
"""
Script para debuggear el problema del navbar
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category
from store.context_processors import categories
from django.utils.text import slugify
from django.http import HttpRequest

def test_navbar_context():
    """Test del context processor y slugify para el navbar"""
    
    print("🔧 DEBUGGING NAVBAR CONTEXT")
    print("=" * 50)
    
    # Simular request
    request = HttpRequest()
    context = categories(request)
    
    print(f"📊 Categorías en context: {len(context['categories'])}")
    print()
    
    for category in context['categories']:
        print(f"🏷️  Categoría: {category.name}")
        print(f"   Slug: {slugify(category.name)}")
        print(f"   Activa: {category.is_active}")
        
        subcats = category.subcategories.filter(is_active=True)
        print(f"   Subcategorías activas: {subcats.count()}")
        
        for subcat in subcats:
            print(f"      - {subcat.name}")
            print(f"        Slug: {slugify(subcat.name)}")
            print(f"        URL esperada: /category/{slugify(category.name)}/{slugify(subcat.name)}/")
        print()

def test_bootstrap_js():
    """Verificar que Bootstrap JS esté funcionando"""
    print("🎨 VERIFICANDO BOOTSTRAP")
    print("=" * 30)
    print("Verificar en el navegador:")
    print("1. ¿Se cargan los archivos CSS/JS de Bootstrap?")
    print("2. ¿Funciona el dropdown al hacer hover/click?")
    print("3. ¿Hay errores en la consola del navegador?")

if __name__ == '__main__':
    test_navbar_context()
    test_bootstrap_js()
