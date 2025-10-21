"""
Script para poblar productos con stock para pruebas del sistema de reservas
Ejecutar: python manage.py shell < populate_stock.py
"""

from store.models import Product

# Actualizar productos existentes con stock
products = Product.objects.all()

stock_data = [
    {'name_contains': 'rifle', 'stock': 5},
    {'name_contains': 'pistol', 'stock': 8},
    {'name_contains': 'municion', 'stock': 100},
    {'name_contains': 'scope', 'stock': 3},
    {'name_contains': 'holster', 'stock': 12},
]

# Asignar stock a productos existentes
for product in products:
    if not hasattr(product, 'stock') or product.stock == 0:
        # Asignar stock basado en el nombre del producto
        assigned = False
        for stock_info in stock_data:
            if stock_info['name_contains'].lower() in product.name.lower():
                product.stock = stock_info['stock']
                assigned = True
                break
        
        if not assigned:
            # Asignar stock aleatorio entre 1 y 20
            import random
            product.stock = random.randint(1, 20)
        
        product.is_available = True
        product.save()
        print(f"Actualizado {product.name}: Stock = {product.stock}")

print(f"Se actualizaron {products.count()} productos con stock")
