#!/usr/bin/env python3
"""
Script para generar un archivo de test HTML y verificar la renderización
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from payment.forms import ShippingMethodForm
from django.template import Template, Context

def generate_test_html():
    print("🔧 Generando HTML de test...")
    
    # Crear formulario
    form = ShippingMethodForm(cart_total=10000)
    
    # Template básico para probar
    template_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test Shipping Form</title>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        console.log('🚀 DOM loaded');
        const radios = document.querySelectorAll('input[name="shipping_method"]');
        console.log('📻 Radio buttons found:', radios.length);
        
        radios.forEach((radio, index) => {
            console.log(`Radio ${index}: value=${radio.value}, name=${radio.name}`);
            radio.addEventListener('change', function() {
                console.log('🔄 Radio changed:', this.value);
                const cost = this.value == '1' ? 3000 : (this.value == '2' ? 3600 : 2400);
                document.getElementById('total').textContent = `Total: ${10000 + cost}`;
            });
        });
    });
    </script>
</head>
<body>
    <h1>Test Shipping Method Form</h1>
    <form>
        <div class="shipping-options">
            {{ form.shipping_method }}
        </div>
    </form>
    <p id="total">Total: 10000</p>
    
    <h2>Debug Info:</h2>
    <pre id="debug"></pre>
    <script>
        document.getElementById('debug').textContent = document.querySelector('.shipping-options').innerHTML;
    </script>
</body>
</html>
'''
    
    template = Template(template_content)
    context = Context({'form': form})
    html_content = template.render(context)
    
    # Escribir archivo de test
    with open('/Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce/test_form.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Archivo test_form.html generado")
    print("📂 Ubicación: /Users/alexisplescia/Desktop/git_app_sniper/django_ecommerce/test_form.html")
    print("🌐 Abre el archivo en el navegador para probar")

if __name__ == '__main__':
    generate_test_html()
