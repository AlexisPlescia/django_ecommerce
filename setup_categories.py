#!/usr/bin/env python3
"""
Script para configurar categorías y subcategorías iniciales
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from store.models import Category, Product

def setup_categories():
    """Configurar categorías y subcategorías iniciales"""
    
    # 1. Crear categoría principal "Armas"
    armas_category, created = Category.objects.get_or_create(
        name="Armas", 
        defaults={
            'parent': None, 
            'is_active': True,
            'description': 'Categoría principal de armas de fuego'
        }
    )
    print(f"✓ Categoría 'Armas': {'creada' if created else 'ya existe'}")

    # 2. Crear subcategorías
    subcategories = [
        ("Armas nuevas", "Armas de fuego nuevas sin uso"),
        ("Armas usadas", "Armas de fuego de segunda mano en buen estado"),
    ]
    
    for name, description in subcategories:
        subcategory, created = Category.objects.get_or_create(
            name=name,
            parent=armas_category,
            defaults={
                'is_active': True,
                'description': description
            }
        )
        print(f"✓ Subcategoría '{name}': {'creada' if created else 'ya existe'}")

    # 3. Verificar productos existentes y reasignar si es necesario
    products_without_subcategory = Product.objects.filter(category=armas_category)
    
    if products_without_subcategory.exists():
        print(f"\n📦 Encontrados {products_without_subcategory.count()} productos sin subcategoría")
        
        # Reasignar algunos productos a subcategorías para testing
        armas_nuevas = Category.objects.get(name="Armas nuevas", parent=armas_category)
        armas_usadas = Category.objects.get(name="Armas usadas", parent=armas_category)
        
        # Asignar la mitad a "nuevas" y la mitad a "usadas"
        products_list = list(products_without_subcategory)
        middle = len(products_list) // 2
        
        for i, product in enumerate(products_list):
            if i < middle:
                product.category = armas_nuevas
                product.save()
                print(f"  → {product.name} → Armas nuevas")
            else:
                product.category = armas_usadas
                product.save()
                print(f"  → {product.name} → Armas usadas")

    # 4. Mostrar resumen final
    print(f"\n📊 RESUMEN:")
    print(f"• Categoría 'Armas': {Product.objects.filter(category=armas_category).count()} productos")
    print(f"• Subcategoría 'Armas nuevas': {Product.objects.filter(category__name='Armas nuevas').count()} productos")
    print(f"• Subcategoría 'Armas usadas': {Product.objects.filter(category__name='Armas usadas').count()} productos")
    
    return True

if __name__ == "__main__":
    print("🚀 Configurando categorías y subcategorías...")
    try:
        setup_categories()
        print("\n✅ Configuración completada exitosamente!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
