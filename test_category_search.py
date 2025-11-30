#!/usr/bin/env python
"""
Script para probar las mejoras en búsqueda de subcategorías
"""

import os
import django
import sys

# Add the project directory to the Python path
sys.path.append('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category
from store.views import normalize_text, find_category_by_name

def test_category_search():
    """Probar la nueva función de búsqueda robusta"""
    
    print("🧪 PROBANDO BÚSQUEDA ROBUSTA DE CATEGORÍAS")
    print("=" * 60)
    
    test_cases = [
        # (slug_name, expected_name, parent_slug)
        ('servicios', 'SERVICIOS', None),
        ('taller de reparacion', 'Taller de reparación', 'SERVICIOS'),
        ('taller-de-reparacion', 'Taller de reparación', 'SERVICIOS'),
        ('certificaciones de armas de fuego', 'Certificaciones de armas de fuego', 'SERVICIOS'),
        ('armas', 'ARMAS', None),
        ('accesorios', 'ACCESORIOS', None),
    ]
    
    for search_name, expected_name, parent_name in test_cases:
        print(f"\n🔍 Buscando: '{search_name}'")
        
        if parent_name:
            parent = find_category_by_name(parent_name)
            if parent:
                print(f"   En categoría padre: {parent.name}")
                category = find_category_by_name(search_name, parent=parent)
            else:
                print(f"   ❌ Padre '{parent_name}' no encontrado")
                continue
        else:
            category = find_category_by_name(search_name)
        
        if category:
            print(f"   ✅ Encontrada: '{category.name}'")
            if expected_name:
                if category.name == expected_name:
                    print(f"   ✅ Coincide con lo esperado")
                else:
                    print(f"   ⚠️  Esperado: '{expected_name}', Encontrado: '{category.name}'")
        else:
            print(f"   ❌ NO encontrada")
    
    print("\n" + "=" * 60)
    print("🎯 PROBANDO URLs PROBLEMÁTICAS:")
    
    # Test URLs que fallaban antes
    problematic_urls = [
        '/category/servicios/taller-de-reparacion/',
        '/category/servicios/certificaciones-de-armas-de-fuego/',
        '/category/armas/armas-cortas/',
        '/category/accesorios/cachas-para-pistolas/',
    ]
    
    for url in problematic_urls:
        print(f"\n🔗 URL: {url}")
        # Simular el parsing de URL
        parts = url.strip('/').split('/')
        if len(parts) >= 3 and parts[0] == 'category':
            parent_slug = parts[1]
            subcat_slug = parts[2]
            
            parent_name = parent_slug.replace('-', ' ')
            subcat_name = subcat_slug.replace('-', ' ')
            
            parent = find_category_by_name(parent_name)
            if parent:
                subcat = find_category_by_name(subcat_name, parent=parent)
                if subcat:
                    print(f"   ✅ Resuelve a: {parent.name} > {subcat.name}")
                else:
                    print(f"   ❌ Subcategoría '{subcat_name}' no encontrada")
            else:
                print(f"   ❌ Categoría padre '{parent_name}' no encontrada")

if __name__ == '__main__':
    test_category_search()
