# E2E Testing Framework - QA Manual y Automatización

## 📋 Descripción
Framework completo de testing para ecommerce Django con enfoque en QA manual y automatización. Incluye tests de UI, API, seguridad, rendimiento y accesibilidad.

## 🗂️ Estructura del Proyecto

```
e2e_test/
├── pages/              # Page Object Model
│   ├── base_page.py   # Clase base para todos los page objects
│   ├── home_page.py   # Page object para página principal
│   ├── login_page.py  # Page object para login
│   ├── register_page.py # Page object para registro
│   └── cart_page.py   # Page object para carrito
├── ui_tests/          # Tests de interfaz de usuario
│   ├── test_authentication.py # Tests de login/registro
│   └── test_ecommerce.py      # Tests generales de ecommerce
├── api_tests/         # Tests de API
│   └── test_api.py    # Tests de endpoints y API
├── utils/             # Utilidades y helpers
│   └── test_helpers.py # Funciones helper para tests
├── test_data/         # Datos de prueba
│   └── test_config.py # Configuración y datos de tests
├── reports/           # Directorio para reportes
│   └── screenshots/   # Screenshots de tests fallidos
├── conftest.py        # Configuración global de pytest
├── requirements_test.txt # Dependencias de testing
└── run_tests.py       # Script para ejecutar tests
```

## 🚀 Instalación

### 1. Instalar dependencias
```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias de testing
pip install -r e2e_test/requirements_test.txt
```

### 2. Configurar ChromeDriver
El framework usa `webdriver-manager` para manejar automáticamente ChromeDriver, no necesitas instalarlo manualmente.

## 📊 Ejecución de Tests

### Comandos Básicos

```bash
# Ejecutar todos los tests
pytest e2e_test/

# Ejecutar solo smoke tests (críticos)
pytest e2e_test/ -m smoke

# Ejecutar tests de regresión
pytest e2e_test/ -m regression

# Ejecutar solo tests de UI
pytest e2e_test/ -m ui

# Ejecutar solo tests de API
pytest e2e_test/ -m api

# Ejecutar solo tests de autenticación
pytest e2e_test/ -m auth
```

### Script de Ejecución Avanzado

```bash
# Usando el script personalizado
python e2e_test/run_tests.py --smoke --verbose
python e2e_test/run_tests.py --regression --parallel --headless
python e2e_test/run_tests.py --ui --browser chrome --report html
```

### Opciones del Script

- `--smoke`: Ejecutar solo smoke tests
- `--regression`: Ejecutar regression tests
- `--ui`: Ejecutar solo UI tests
- `--api`: Ejecutar solo API tests
- `--auth`: Ejecutar tests de autenticación
- `--security`: Ejecutar tests de seguridad
- `--parallel`: Ejecutar tests en paralelo
- `--headless`: Ejecutar en modo headless
- `--browser`: Elegir browser (chrome/firefox)
- `--report`: Formato de reporte (html/json/junit)

## 📈 Reportes

### Reportes HTML
```bash
pytest e2e_test/ --html=reports/report.html --self-contained-html
```

### Reportes con Cobertura
```bash
pytest e2e_test/ --cov=e2e_test --cov-report=html:reports/coverage
```

### Reportes JUnit (para CI/CD)
```bash
pytest e2e_test/ --junit-xml=reports/junit.xml
```

## 🧪 Tipos de Tests Incluidos

### 1. **Tests de Autenticación**
- ✅ Login exitoso
- ✅ Login con credenciales inválidas
- ✅ Registro de usuario
- ✅ Validación de contraseñas
- ✅ Protección contra inyección SQL
- ✅ Protección contra XSS

### 2. **Tests de Funcionalidad**
- ✅ Navegación principal
- ✅ Visualización de productos
- ✅ Búsqueda de productos
- ✅ Categorías
- ✅ Carrito de compras
- ✅ Responsive design

### 3. **Tests de API**
- ✅ Endpoints principales
- ✅ Códigos de estado HTTP
- ✅ Archivos estáticos
- ✅ Protección CSRF
- ✅ Tiempos de respuesta
- ✅ Headers de seguridad

### 4. **Tests de Seguridad**
- ✅ Inyección SQL
- ✅ Cross-Site Scripting (XSS)
- ✅ Protección CSRF
- ✅ Autenticación/Autorización
- ✅ Validación de entrada

### 5. **Tests de Rendimiento**
- ✅ Tiempos de carga de página
- ✅ Tiempos de respuesta
- ✅ Tamaño de página
- ✅ Optimización de recursos

## 📱 Marcadores de Tests

Los tests están organizados con marcadores para facilitar la ejecución:

- `@pytest.mark.smoke` - Tests críticos
- `@pytest.mark.regression` - Tests de regresión
- `@pytest.mark.ui` - Tests de interfaz
- `@pytest.mark.api` - Tests de API
- `@pytest.mark.auth` - Tests de autenticación
- `@pytest.mark.security` - Tests de seguridad
- `@pytest.mark.performance` - Tests de rendimiento

## 🔧 Configuración

### Configuración en `conftest.py`
```python
BASE_URL = "http://127.0.0.1:8001"
TIMEOUT = 10
SCREENSHOT_DIR = "e2e_test/reports/screenshots"
```

### Configuración en `pytest.ini`
```ini
[tool:pytest]
testpaths = e2e_test
python_files = test_*.py
addopts = -v --tb=short --html=reports/report.html
```

## 📸 Screenshots Automáticos

El framework toma screenshots automáticamente cuando:
- Un test falla
- Se llama manualmente con `test_helpers.take_screenshot()`
- Se usa el método `take_screenshot()` en page objects

## 🎯 Casos de Uso para Entrevista QA

### Demostrar Conocimientos de:

1. **Page Object Model (POM)**
   - Separación de responsabilidades
   - Mantenibilidad del código
   - Reutilización de elementos

2. **Pytest Framework**
   - Fixtures
   - Marcadores
   - Parametrización
   - Reportes

3. **Selenium WebDriver**
   - Locators
   - Waits
   - Actions
   - JavaScript execution

4. **Testing Best Practices**
   - AAA pattern (Arrange, Act, Assert)
   - Independent tests
   - Data-driven testing
   - Error handling

5. **CI/CD Integration**
   - JUnit reports
   - Parallel execution
   - Headless testing
   - Environment configuration

## 🛠️ Extensibilidad

### Agregar Nuevos Tests
1. Crear nuevo archivo en `ui_tests/` o `api_tests/`
2. Usar page objects existentes o crear nuevos
3. Agregar marcadores apropiados
4. Documentar el propósito del test

### Agregar Nuevos Page Objects
1. Heredar de `BasePage`
2. Definir locators como constantes
3. Implementar métodos de acción
4. Agregar métodos de verificación

### Personalizar Configuración
- Modificar `conftest.py` para fixtures globales
- Actualizar `test_config.py` para datos de prueba
- Ajustar `pytest.ini` para comportamiento de pytest

## 🐛 Debugging

### Modo Debug
```bash
# Ejecutar con pdb
pytest e2e_test/ --pdb

# Ejecutar con modo verbose
pytest e2e_test/ -v -s

# Ejecutar test específico
pytest e2e_test/ui_tests/test_authentication.py::TestAuthentication::test_login_page_loads_correctly -v
```

### Screenshots de Debug
```python
# En cualquier test
def test_example(self, driver, test_helpers):
    test_helpers.take_screenshot(driver, "debug_screenshot")
```

## 📋 Checklist para Entrevista

### ✅ Preparación
- [ ] Servidor Django corriendo
- [ ] Dependencias instaladas
- [ ] Chrome instalado
- [ ] Tests ejecutándose correctamente

### ✅ Demostración
- [ ] Explicar estructura del framework
- [ ] Mostrar ejecución de smoke tests
- [ ] Demostrar diferentes tipos de tests
- [ ] Mostrar reportes generados
- [ ] Explicar Page Object Model
- [ ] Demostrar debugging

### ✅ Conceptos QA
- [ ] Diferencia entre QA manual y automatizado
- [ ] Cuándo usar cada tipo de test
- [ ] Estrategias de testing
- [ ] Manejo de datos de prueba
- [ ] Integración con CI/CD

## 🎓 Recursos Adicionales

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://martinfowler.com/bliki/PageObject.html)
- [Testing Best Practices](https://testautomationu.applitools.com/)

## 📞 Soporte

Para dudas sobre el framework o mejoras:
1. Revisar documentación en código
2. Consultar logs de ejecución
3. Verificar configuración en `conftest.py`
4. Revisar datos de prueba en `test_config.py`
