from .models import Category

def categories(request):
    """
    Context processor para hacer que las categorías estén disponibles en todos los templates
    """
    # Obtener solo las categorías principales (sin padre)
    parent_categories = Category.objects.filter(parent=None, is_active=True).order_by('name')
    
    return {
        'categories': parent_categories
    }
