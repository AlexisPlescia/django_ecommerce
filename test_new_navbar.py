#!/usr/bin/env python
"""
Script para verificar el nuevo navbar simplificado
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category
from django.utils.text import slugify

def test_new_navbar():
    """Test del nuevo navbar simplificado"""
    
    print("🧪 VERIFICANDO NUEVO NAVBAR SIMPLIFICADO")
    print("=" * 50)
    
    # Categorías principales
    categories = Category.objects.filter(parent=None, is_active=True).order_by('name')
    
    print(f"📊 Total de categorías principales: {categories.count()}")
    print()
    
    print("📋 ESTRUCTURA DEL DROPDOWN:")
    print("1. 🎯 Todos los productos")
    print("   → URL: /category_summary/")
    print()
    
    for i, category in enumerate(categories, 2):
        print(f"{i}. 📁 {category.name}")
        slug = slugify(category.name)
        print(f"   → URL: /category/{slug}")
        print(f"   → Subcategorías: {category.subcategories.filter(is_active=True).count()}")
        print()
    
    print("✅ VENTAJAS DEL NUEVO DESIGN:")
    print("- Más simple y directo")
    print("- Menos sobrecargado visualmente") 
    print("- Fácil acceso a 'Todos los productos'")
    print("- Solo categorías principales (más limpio)")
    print("- Usuario puede explorar subcategorías en la página de categoría")

if __name__ == '__main__':
    test_new_navbar()
