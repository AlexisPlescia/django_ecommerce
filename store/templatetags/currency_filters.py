from django import template
from decimal import Decimal, InvalidOperation
import locale

register = template.Library()

@register.filter
def currency_no_decimals(value):
    """
    Convierte un valor numérico a formato de moneda argentina sin decimales.
    Ejemplo: 1500.00 -> $1.500
    """
    if value is None or value == '':
        return '$0'
    
    try:
        # Convertir a Decimal para manejar correctamente los números
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Redondear a entero (sin decimales)
        value = int(value)
        
        # Formatear con separadores de miles (punto)
        formatted_value = f"{value:,}".replace(',', '.')
        
        return f"${formatted_value}"
    
    except (ValueError, TypeError, InvalidOperation):
        return '$0'

@register.filter  
def currency(value):
    """
    Convierte un valor numérico a formato de moneda argentina con decimales.
    Ejemplo: 1500.50 -> $1.500,50
    """
    if value is None or value == '':
        return '$0,00'
    
    try:
        # Convertir a Decimal para manejar correctamente los números
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Separar parte entera y decimal
        integer_part = int(value)
        decimal_part = int((value - integer_part) * 100)
        
        # Formatear parte entera con separadores de miles (punto)
        formatted_integer = f"{integer_part:,}".replace(',', '.')
        
        # Formatear parte decimal con coma
        return f"${formatted_integer},{decimal_part:02d}"
    
    except (ValueError, TypeError):
        return '$0,00'

@register.filter
def peso_arg(value):
    """
    Alias para currency_no_decimals
    """
    return currency_no_decimals(value)
