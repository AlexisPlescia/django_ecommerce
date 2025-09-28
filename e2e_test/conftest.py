"""
Configuración global para pytest - Testing Framework QA
Este archivo contiene fixtures y configuración común para todos los tests
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime

# Configuración base
BASE_URL = "http://127.0.0.1:8001"
TIMEOUT = 10
SCREENSHOT_DIR = "e2e_test/reports/screenshots"

@pytest.fixture(scope="session")
def browser_config():
    """Configuración del navegador para todos los tests"""
    chrome_options = Options()
    
    # Configuraciones para desarrollo/debug
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Para ejecución en modo headless (comentar para ver el navegador)
    # chrome_options.add_argument("--headless")
    
    # Configuraciones adicionales
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    return chrome_options

@pytest.fixture(scope="function")
def driver(browser_config):
    """Fixture del driver de Selenium con configuración automática"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=browser_config)
    
    # Configuraciones del driver
    driver.implicitly_wait(TIMEOUT)
    driver.maximize_window()
    
    yield driver
    
    # Cleanup - cerrar navegador después de cada test
    driver.quit()

@pytest.fixture(scope="function")
def wait(driver):
    """Fixture para WebDriverWait"""
    return WebDriverWait(driver, TIMEOUT)

@pytest.fixture(scope="function")
def navigate_to_home(driver):
    """Fixture para navegar al home page"""
    driver.get(BASE_URL)
    return driver

@pytest.fixture(scope="function")
def create_screenshot_dir():
    """Crear directorio para screenshots si no existe"""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    return SCREENSHOT_DIR

def pytest_configure(config):
    """Configuración inicial de pytest"""
    # Crear directorio de reportes
    if not os.path.exists("e2e_test/reports"):
        os.makedirs("e2e_test/reports")

def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots en caso de fallo"""
    if call.when == "call":
        if call.excinfo is not None:
            # Test falló, capturar screenshot
            try:
                driver = item.funcargs.get('driver')
                if driver:
                    screenshot_name = f"failed_test_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
                    
                    if not os.path.exists(SCREENSHOT_DIR):
                        os.makedirs(SCREENSHOT_DIR)
                    
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot guardado: {screenshot_path}")
            except Exception as e:
                print(f"Error al capturar screenshot: {e}")

# Fixtures para datos de prueba
@pytest.fixture
def test_user_data():
    """Datos de usuario para pruebas"""
    return {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }

@pytest.fixture
def admin_user_data():
    """Datos de administrador para pruebas"""
    return {
        "username": "admin",
        "password": "admin123"
    }

# Utilidades compartidas
class TestHelpers:
    """Clase con métodos helper para los tests"""
    
    @staticmethod
    def take_screenshot(driver, name):
        """Tomar screenshot con nombre personalizado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{name}_{timestamp}.png"
        screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
        
        if not os.path.exists(SCREENSHOT_DIR):
            os.makedirs(SCREENSHOT_DIR)
        
        driver.save_screenshot(screenshot_path)
        return screenshot_path
    
    @staticmethod
    def wait_for_element(driver, by, value, timeout=TIMEOUT):
        """Esperar por elemento con timeout personalizado"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    @staticmethod
    def wait_for_clickable_element(driver, by, value, timeout=TIMEOUT):
        """Esperar por elemento clickeable"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

@pytest.fixture
def test_helpers():
    """Fixture para acceder a las utilidades helper"""
    return TestHelpers

# Marcadores personalizados para organizar tests
def pytest_configure(config):
    """Configurar marcadores personalizados"""
    config.addinivalue_line("markers", "smoke: marca tests como smoke tests")
    config.addinivalue_line("markers", "regression: marca tests como regression tests")
    config.addinivalue_line("markers", "ui: marca tests como UI tests")
    config.addinivalue_line("markers", "api: marca tests como API tests")
    config.addinivalue_line("markers", "auth: marca tests relacionados con autenticación")
    config.addinivalue_line("markers", "cart: marca tests relacionados con carrito")
    config.addinivalue_line("markers", "checkout: marca tests relacionados con checkout")
