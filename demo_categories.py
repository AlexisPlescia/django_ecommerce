#!/usr/bin/env python3
"""
Script de demostración para mostrar el sistema automatizado de categorías
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from store.models import Category

def demo_automated_categories():
    """Demostrar el sistema automatizado creando categorías de ejemplo"""
    
    print("🚀 Demostración del Sistema Automatizado de Categorías")
    print("=" * 60)
    
    # Ejemplos de categorías que se beneficiarán del sistema automatizado
    demo_categories = [
        {
            "name": "Cuchillos",
            "description": "Cuchillos de diferentes tipos y calidades",
            "subcategories": [
                ("Cuchillos nuevos", "Cuchillos nuevos sin uso"),
                ("Cuchillos usados", "Cuchillos de segunda mano en excelente estado"),
                ("Cuchillos vintage", "Cuchillos clásicos y de colección"),
                ("Cuchillos tácticos", "Cuchillos para uso táctico y militar"),
            ]
        },
        {
            "name": "Ópticas",
            "description": "Miras y equipos ópticos",
            "subcategories": [
                ("Ópticas nuevas", "Miras telescópicas nuevas"),
                ("Ópticas usadas", "Equipos ópticos de segunda mano"),
                ("Ópticas premium", "Equipos ópticos de alta gama"),
                ("Ópticas deportivas", "Miras para competición deportiva"),
            ]
        },
        {
            "name": "Seguridad",
            "description": "Equipos de seguridad y protección",
            "subcategories": [
                ("Seguridad nueva", "Equipos de protección nuevos"),
                ("Seguridad profesional", "Equipos para uso profesional"),
                ("Seguridad básica", "Equipos de protección básicos"),
                ("Seguridad especial", "Equipos especializados"),
            ]
        }
    ]
    
    for cat_data in demo_categories:
        print(f"\n📁 Creando categoría: {cat_data['name']}")
        
        # Crear categoría principal
        main_category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                'parent': None,
                'is_active': True,
                'description': cat_data['description']
            }
        )
        
        status = "✅ NUEVA" if created else "🔄 EXISTE"
        print(f"   {status}: {main_category.name}")
        
        # Crear subcategorías
        for sub_name, sub_desc in cat_data["subcategories"]:
            subcategory, created = Category.objects.get_or_create(
                name=sub_name,
                parent=main_category,
                defaults={
                    'is_active': True,
                    'description': sub_desc
                }
            )
            
            status = "✅ NUEVA" if created else "🔄 EXISTE"
            print(f"     └── {status}: {subcategory.name}")
            
            # Mostrar qué ícono recibirá automáticamente
            icon_demo = get_icon_for_subcategory(sub_name)
            color_demo = get_color_for_subcategory(sub_name)
            print(f"         └── 🎨 Ícono: {icon_demo} | Color: {color_demo}")
    
    print(f"\n🎉 ¡Sistema de categorías automatizado configurado!")
    print("💡 Beneficios del sistema:")
    print("   • Íconos automáticos según palabras clave")
    print("   • Colores específicos por tipo (nuevos=verde, usados=naranja, etc.)")
    print("   • Diseño consistente para todas las categorías")
    print("   • Sin necesidad de configuración manual")
    print("   • Escalable para futuras categorías")

def get_icon_for_subcategory(name):
    """Mostrar qué ícono recibiría una subcategoría"""
    name_lower = name.lower()
    
    if any(word in name_lower for word in ['nuevas', 'nuevos', 'nuevo', 'nueva']):
        return "⭐ fa-star (Nuevo)"
    elif any(word in name_lower for word in ['usadas', 'usados', 'usado', 'usada']):
        return "♻️ fa-recycle (Usado)"
    elif any(word in name_lower for word in ['vintage', 'antiguas', 'clasicas']):
        return "👑 fa-crown (Vintage)"
    elif any(word in name_lower for word in ['premium', 'lujo', 'profesional']):
        return "💎 fa-gem (Premium)"
    elif any(word in name_lower for word in ['economicas', 'basicas', 'entrada']):
        return "💲 fa-dollar-sign (Económico)"
    elif any(word in name_lower for word in ['deportivas', 'competicion', 'sport']):
        return "🏆 fa-trophy (Deportivo)"
    elif any(word in name_lower for word in ['tacticas', 'militar']):
        return "🛡️ fa-shield-alt (Táctico)"
    elif any(word in name_lower for word in ['especiales', 'coleccion']):
        return "📜 fa-certificate (Especial)"
    else:
        return "📂 fa-layer-group (General)"

def get_color_for_subcategory(name):
    """Mostrar qué color recibiría una subcategoría"""
    name_lower = name.lower()
    
    if any(word in name_lower for word in ['nuevas', 'nuevos']):
        return "🟢 Verde (Nuevos)"
    elif any(word in name_lower for word in ['usadas', 'usados']):
        return "🟠 Naranja (Usados)"
    elif any(word in name_lower for word in ['vintage', 'antiguas']):
        return "🟤 Marrón (Vintage)"
    else:
        return "🔵 Azul (Estándar)"

if __name__ == "__main__":
    demo_automated_categories()
