"""
Datos de prueba para tests
"""

# Datos de usuarios de prueba
TEST_USERS = [
    {
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    },
    {
        "username": "testuser2",
        "email": "testuser2@example.com",
        "password": "TestPassword456!",
        "first_name": "Another",
        "last_name": "User"
    }
]

# Datos de administrador
ADMIN_USER = {
    "username": "admin",
    "password": "admin123"
}

# Datos de productos de prueba
TEST_PRODUCTS = [
    {
        "name": "Producto de Prueba 1",
        "price": 29.99,
        "description": "Descripción del producto de prueba 1"
    },
    {
        "name": "Producto de Prueba 2",
        "price": 49.99,
        "description": "Descripción del producto de prueba 2"
    }
]

# Datos de categorías de prueba
TEST_CATEGORIES = [
    "Electrónicos",
    "Ropa",
    "Hogar",
    "Deportes"
]

# Datos para pruebas de validación
VALIDATION_DATA = {
    "weak_passwords": [
        "123",
        "password",
        "12345678",
        "qwerty",
        "abc123"
    ],
    "invalid_emails": [
        "email_sin_arroba",
        "@dominio.com",
        "usuario@",
        "usuario.dominio.com",
        "usuario@dominio",
        "usuario@@dominio.com"
    ],
    "sql_injection_attempts": [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users --",
        "admin'--"
    ],
    "xss_attempts": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>"
    ]
}

# Configuración de tests
TEST_CONFIG = {
    "base_url": "http://127.0.0.1:8001",
    "timeout": 10,
    "screenshot_dir": "e2e_test/reports/screenshots",
    "report_dir": "e2e_test/reports",
    "browser": "chrome",
    "headless": False,
    "window_size": (1920, 1080)
}

# Textos esperados en español
SPANISH_TEXTS = {
    "login": [
        "Iniciar Sesión",
        "Nombre de Usuario",
        "Contraseña"
    ],
    "register": [
        "Registrarse",
        "Nombre",
        "Apellido",
        "Correo Electrónico",
        "Confirmar Contraseña"
    ],
    "navigation": [
        "Inicio",
        "Categorías",
        "Carrito",
        "Cerrar Sesión"
    ],
    "messages": [
        "error",
        "éxito",
        "contraseña",
        "usuario"
    ]
}

# Selectores CSS comunes
CSS_SELECTORS = {
    "buttons": {
        "login": "button[type='submit']",
        "register": "button[type='submit']",
        "add_to_cart": ".btn-primary",
        "checkout": ".btn-success"
    },
    "forms": {
        "login": "form",
        "register": "form",
        "search": "form"
    },
    "navigation": {
        "navbar": ".navbar",
        "menu_items": ".nav-item",
        "dropdown": ".dropdown"
    },
    "products": {
        "product_card": ".card",
        "product_title": ".card-title",
        "product_price": ".card-text",
        "product_image": ".card-img-top"
    },
    "cart": {
        "cart_item": ".cart-item",
        "quantity": ".quantity-input",
        "remove_button": ".remove-item",
        "total": ".total"
    },
    "messages": {
        "success": ".alert-success",
        "error": ".alert-danger",
        "warning": ".alert-warning",
        "info": ".alert-info"
    }
}

# URLs de la aplicación
URLS = {
    "home": "/",
    "login": "/login",
    "register": "/register",
    "cart": "/cart",
    "search": "/search",
    "logout": "/logout",
    "admin": "/admin/",
    "shipped_orders": "/shipped_dash",
    "not_shipped_orders": "/not_shipped_dash"
}

# Datos de rendimiento esperados
PERFORMANCE_THRESHOLDS = {
    "page_load_time": 5.0,  # segundos
    "element_load_time": 2.0,  # segundos
    "max_page_size": 1024 * 1024,  # 1MB
    "api_response_time": 3.0  # segundos
}

# Configuración de browsers
BROWSER_CONFIG = {
    "chrome": {
        "driver_path": None,  # Se usa webdriver-manager
        "options": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1920,1080"
        ]
    },
    "firefox": {
        "driver_path": None,
        "options": [
            "--width=1920",
            "--height=1080"
        ]
    }
}

# Configuración de reportes
REPORT_CONFIG = {
    "formats": ["html", "json"],
    "include_screenshots": True,
    "include_logs": True,
    "include_performance": True
}

# Datos de accesibilidad
ACCESSIBILITY_CONFIG = {
    "required_alt_attributes": True,
    "required_aria_labels": True,
    "color_contrast_ratio": 4.5,
    "keyboard_navigation": True
}

# Configuración de seguridad
SECURITY_CONFIG = {
    "test_sql_injection": True,
    "test_xss": True,
    "test_csrf_protection": True,
    "test_authentication": True,
    "test_authorization": True
}

# Datos de internacionalización
I18N_CONFIG = {
    "default_language": "es",
    "supported_languages": ["es", "en"],
    "required_translations": SPANISH_TEXTS
}
