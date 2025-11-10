from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def subcategory_icon(subcategory_name):
    """
    Genera un ícono específico basado en el nombre de la subcategoría.
    Sistema automatizado que detecta palabras clave.
    """
    name_lower = subcategory_name.lower()
    
    # Diccionario de patrones e íconos
    icon_patterns = {
        # Nuevos/Nuevas
        ('nuevas', 'nuevos', 'nuevo', 'nueva'): 'fas fa-crosshairs',
        
        # Usados/Usadas/Segunda mano
        ('usadas', 'usados', 'usado', 'usada', 'segunda', 'mano'): 'fas fa-gun',
        
        # Vintage/Antiguas/Clásicas
        ('vintage', 'antiguas', 'antiguos', 'clasicas', 'clasicos', 'retro'): 'fas fa-chess-rook',
        
        # Premium/Lujo/Profesional
        ('premium', 'lujo', 'profesional', 'profesionales', 'elite'): 'fas fa-star',
        
        # Económicas/Básicas/Entrada
        ('economicas', 'economicos', 'basicas', 'basicos', 'entrada'): 'fas fa-circle',
        
        # Deportivas/Competición
        ('deportivas', 'deportivos', 'competicion', 'sport'): 'fas fa-bullseye',
        
        # Tácticas/Militares
        ('tacticas', 'tacticos', 'militar', 'militares'): 'fas fa-shield-alt',
        
        # Especiales/Colección
        ('especiales', 'coleccion', 'edicion', 'limitada'): 'fas fa-certificate',
    }
    
    # Buscar coincidencias
    for keywords, icon in icon_patterns.items():
        if any(keyword in name_lower for keyword in keywords):
            return mark_safe(f'<i class="{icon}"></i>')
    
    # Íconos por categoría padre si no encuentra subcategoría específica
    category_icons = {
        'armas': 'fas fa-crosshairs',
        'cuchillos': 'fas fa-cut',
        'municiones': 'fas fa-circle',
        'accesorios': 'fas fa-cogs',
        'mantenimiento': 'fas fa-tools',
        'opticas': 'fas fa-eye',
        'holsters': 'fas fa-vest',
        'seguridad': 'fas fa-lock',
    }
    
    # Si es una subcategoría, intentar detectar la categoría padre por palabras clave
    for category, icon in category_icons.items():
        if category in name_lower:
            return mark_safe(f'<i class="{icon}"></i>')
    
    # Ícono por defecto
    return mark_safe('<i class="fas fa-layer-group"></i>')

@register.filter
def subcategory_data_type(subcategory_name):
    """
    Genera un atributo data-type para CSS específico
    """
    return subcategory_name.lower().replace(' ', '-')
