#!/usr/bin/env python
"""
Seed script para cargar categorías y subcategorías de Armería Sniper
Ejecutar con: python seed_categories.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category

def create_categories():
    """
    Crea todas las categorías y subcategorías de Armería Sniper
    """
    
    # Definir estructura de categorías
    categories_data = {
        'SERVICIOS': [
            'Taller de reparación',
            'Certificaciones de armas de fuego',
            'Tasaciones para sucesiones',
            'Estudio criminalístico forense'
        ],
        
        'ARMAS': [
            'Armas Cortas',
            'Armas Largas',
            'Pistolones',
            'Armas Combinadas',
            'Armas de Proyección (Venta libre)',
            'Aire Comprimido / PCP / CO2 (Venta Libre)',
            'Armas de Colección (Venta libre)',
            'Armas Raras / Difíciles de conseguir',
            'Armas Nacionales Históricas',
            'Armas No Letales (Venta libre)'
        ],
        
        'ACCESORIOS': [
            'Cachas para Pistolas',
            'Cachas para Revólveres',
            'Cachas para Restauraciones',
            'Cargadores Nuevos',
            'Cargadores Usados',
            'Aparatos de Puntería',
            'Fundas y Portas',
            'Estuches',
            'Linternas y Láser',
            'Mantenimiento de Armas',
            'Accesorios para Tiradores'
        ],
        
        'COLECCIONISMO': [
            'Militaría y Coleccionismo',
            'Libros y Manuales'
        ],
        
        'CONSUMIBLES': [
            'Recarga y Limpieza'
        ]
    }
    
    print("🚀 Iniciando carga de categorías...")
    print("=" * 50)
    
    created_categories = 0
    created_subcategories = 0
    
    for category_name, subcategory_list in categories_data.items():
        
        # Crear categoría principal
        parent_category, created = Category.objects.get_or_create(
            name=category_name,
            parent=None,
            defaults={
                'description': f'Categoría principal: {category_name}',
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Categoría creada: {category_name}")
            created_categories += 1
        else:
            print(f"📁 Categoría existente: {category_name}")
        
        # Crear subcategorías
        for subcategory_name in subcategory_list:
            subcategory, created = Category.objects.get_or_create(
                name=subcategory_name,
                parent=parent_category,
                defaults={
                    'description': f'Subcategoría de {category_name}',
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ✅ Subcategoría creada: {subcategory_name}")
                created_subcategories += 1
            else:
                print(f"  📄 Subcategoría existente: {subcategory_name}")
    
    print("=" * 50)
    print(f"🎉 PROCESO COMPLETADO:")
    print(f"   📁 Categorías principales creadas: {created_categories}")
    print(f"   📄 Subcategorías creadas: {created_subcategories}")
    print(f"   📊 Total de categorías principales: {Category.objects.filter(parent=None).count()}")
    print(f"   📊 Total de subcategorías: {Category.objects.filter(parent__isnull=False).count()}")

def show_category_tree():
    """
    Muestra el árbol de categorías creado
    """
    print("\n🌳 ÁRBOL DE CATEGORÍAS CREADO:")
    print("=" * 50)
    
    parent_categories = Category.objects.filter(parent=None, is_active=True).order_by('name')
    
    for parent in parent_categories:
        print(f"📁 {parent.name}")
        
        subcategories = parent.subcategories.filter(is_active=True).order_by('name')
        for i, sub in enumerate(subcategories):
            connector = "└──" if i == len(subcategories) - 1 else "├──"
            print(f"    {connector} {sub.name}")
        print()

def main():
    """
    Función principal
    """
    try:
        create_categories()
        show_category_tree()
        
        print("✅ ¡Todas las categorías han sido cargadas exitosamente!")
        print("\n🔍 Puedes verificar en el panel de administración:")
        print("   👉 /admin/store/category/")
        
    except Exception as e:
        print(f"❌ Error durante la carga: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
