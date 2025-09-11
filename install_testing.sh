#!/bin/bash

# Script de instalación para framework de testing E2E
echo "🚀 Instalando framework de testing E2E..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Ejecuta este script desde el directorio raíz del proyecto Django"
    exit 1
fi

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
else
    echo "⚠️  No se encontró entorno virtual. Por favor, créalo primero:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    exit 1
fi

# Instalar dependencias de testing
echo "📚 Instalando dependencias de testing..."
pip install pytest>=7.0.0
pip install pytest-html>=3.1.0
pip install pytest-cov>=4.0.0
pip install selenium>=4.0.0
pip install webdriver-manager>=4.0.0
pip install requests>=2.28.0
pip install beautifulsoup4>=4.11.0

# Verificar instalación de Chrome
echo "🔍 Verificando Chrome..."
if command -v google-chrome &> /dev/null; then
    echo "✅ Chrome encontrado"
elif command -v chromium-browser &> /dev/null; then
    echo "✅ Chromium encontrado"
else
    echo "⚠️  Chrome no encontrado. Por favor, instala Chrome o Chromium."
    echo "   Ubuntu/Debian: sudo apt-get install google-chrome-stable"
    echo "   macOS: brew install --cask google-chrome"
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p e2e_test/reports
mkdir -p e2e_test/reports/screenshots

# Hacer ejecutable el script de tests
chmod +x e2e_test/run_tests.py

# Verificar que el servidor Django funciona
echo "🔧 Verificando servidor Django..."
if python manage.py check --deploy; then
    echo "✅ Configuración de Django OK"
else
    echo "⚠️  Hay problemas con la configuración de Django"
fi

# Ejecutar un test básico
echo "🧪 Ejecutando test básico..."
if python -m pytest e2e_test/ui_tests/test_authentication.py::TestAuthentication::test_login_page_loads_correctly -v; then
    echo "✅ Test básico ejecutado exitosamente"
else
    echo "⚠️  El test básico falló. Verifica la configuración."
fi

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📖 Para usar el framework:"
echo "   # Ejecutar todos los tests"
echo "   pytest e2e_test/"
echo ""
echo "   # Ejecutar smoke tests"
echo "   pytest e2e_test/ -m smoke"
echo ""
echo "   # Usar script personalizado"
echo "   python e2e_test/run_tests.py --smoke --verbose"
echo ""
echo "   # Ver reportes HTML"
echo "   pytest e2e_test/ --html=reports/report.html --self-contained-html"
echo ""
echo "📚 Documentación completa en: e2e_test/README.md"
