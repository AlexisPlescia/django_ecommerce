"""
Utilidades para tests - Funciones helper comunes
"""
import time
import random
import string
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDataGenerator:
    """Generador de datos de prueba"""
    
    @staticmethod
    def generate_random_string(length=10):
        """Generar string aleatorio"""
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    @staticmethod
    def generate_random_email():
        """Generar email aleatorio"""
        username = TestDataGenerator.generate_random_string(8)
        domain = TestDataGenerator.generate_random_string(5)
        return f"{username}@{domain}.com"
    
    @staticmethod
    def generate_test_user():
        """Generar datos de usuario de prueba"""
        return {
            "username": f"testuser_{int(time.time())}",
            "email": TestDataGenerator.generate_random_email(),
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
    
    @staticmethod
    def generate_weak_passwords():
        """Generar lista de contraseñas débiles para testing"""
        return [
            "123",
            "password",
            "12345678",
            "qwerty",
            "abc123",
            "test"
        ]
    
    @staticmethod
    def generate_invalid_emails():
        """Generar lista de emails inválidos para testing"""
        return [
            "email_sin_arroba",
            "@dominio.com",
            "usuario@",
            "usuario.dominio.com",
            "usuario@dominio",
            "usuario@@dominio.com",
            "usuario@dominio..com"
        ]
    
    @staticmethod
    def generate_sql_injection_strings():
        """Generar strings para probar inyección SQL"""
        return [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "' OR 1=1 --"
        ]
    
    @staticmethod
    def generate_xss_strings():
        """Generar strings para probar XSS"""
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')></iframe>"
        ]

class ScreenshotHelper:
    """Helper para manejo de screenshots"""
    
    @staticmethod
    def take_screenshot(driver, name, directory="e2e_test/reports/screenshots"):
        """Tomar screenshot con nombre y directorio específico"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(directory, filename)
        
        driver.save_screenshot(filepath)
        return filepath
    
    @staticmethod
    def take_screenshot_on_failure(driver, test_name):
        """Tomar screenshot cuando falla un test"""
        return ScreenshotHelper.take_screenshot(driver, f"FAILED_{test_name}")

class WaitHelper:
    """Helper para waits personalizados"""
    
    @staticmethod
    def wait_for_element_to_be_clickable(driver, locator, timeout=10):
        """Esperar que elemento sea clickeable"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def wait_for_text_in_element(driver, locator, text, timeout=10):
        """Esperar texto específico en elemento"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.text_to_be_present_in_element(locator, text))
    
    @staticmethod
    def wait_for_url_change(driver, current_url, timeout=10):
        """Esperar que cambie la URL"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(lambda d: d.current_url != current_url)
    
    @staticmethod
    def wait_for_page_title(driver, title, timeout=10):
        """Esperar título específico de página"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.title_contains(title))
    
    @staticmethod
    def wait_for_element_to_disappear(driver, locator, timeout=10):
        """Esperar que elemento desaparezca"""
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

class FormHelper:
    """Helper para manejo de formularios"""
    
    @staticmethod
    def fill_form_fields(driver, field_data):
        """Llenar campos de formulario"""
        for field_name, field_value in field_data.items():
            try:
                field = driver.find_element(By.NAME, field_name)
                field.clear()
                field.send_keys(field_value)
            except Exception as e:
                print(f"Error llenando campo {field_name}: {e}")
    
    @staticmethod
    def submit_form(driver, form_locator=None):
        """Enviar formulario"""
        if form_locator:
            form = driver.find_element(*form_locator)
            form.submit()
        else:
            # Buscar botón de submit
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
    
    @staticmethod
    def get_form_errors(driver):
        """Obtener errores de formulario"""
        error_selectors = [
            ".alert-danger",
            ".error",
            ".field-error",
            ".form-error"
        ]
        
        errors = []
        for selector in error_selectors:
            try:
                error_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in error_elements:
                    if element.text.strip():
                        errors.append(element.text.strip())
            except:
                continue
        
        return errors

class NavigationHelper:
    """Helper para navegación"""
    
    @staticmethod
    def navigate_to_page(driver, base_url, path):
        """Navegar a página específica"""
        full_url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        driver.get(full_url)
    
    @staticmethod
    def wait_for_page_load(driver, timeout=30):
        """Esperar que la página cargue completamente"""
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    @staticmethod
    def scroll_to_element(driver, element):
        """Scroll hasta elemento"""
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    @staticmethod
    def get_current_page_info(driver):
        """Obtener información de la página actual"""
        return {
            "url": driver.current_url,
            "title": driver.title,
            "source_length": len(driver.page_source)
        }

class AssertHelper:
    """Helper para assertions personalizadas"""
    
    @staticmethod
    def assert_element_present(driver, locator, message="Element not found"):
        """Assert que elemento esté presente"""
        try:
            driver.find_element(*locator)
            return True
        except:
            raise AssertionError(f"{message}: {locator}")
    
    @staticmethod
    def assert_element_not_present(driver, locator, message="Element should not be present"):
        """Assert que elemento NO esté presente"""
        try:
            driver.find_element(*locator)
            raise AssertionError(f"{message}: {locator}")
        except:
            return True
    
    @staticmethod
    def assert_text_in_page(driver, text, message="Text not found in page"):
        """Assert que texto esté en la página"""
        assert text in driver.page_source, f"{message}: '{text}'"
    
    @staticmethod
    def assert_url_contains(driver, url_part, message="URL doesn't contain expected part"):
        """Assert que URL contenga parte específica"""
        assert url_part in driver.current_url, f"{message}: '{url_part}' not in '{driver.current_url}'"
    
    @staticmethod
    def assert_title_contains(driver, title_part, message="Title doesn't contain expected part"):
        """Assert que título contenga parte específica"""
        assert title_part in driver.title, f"{message}: '{title_part}' not in '{driver.title}'"

class SecurityTestHelper:
    """Helper para tests de seguridad"""
    
    @staticmethod
    def test_sql_injection(driver, form_fields):
        """Probar inyección SQL en formulario"""
        injection_strings = TestDataGenerator.generate_sql_injection_strings()
        
        for injection_string in injection_strings:
            for field_name in form_fields:
                try:
                    field = driver.find_element(By.NAME, field_name)
                    field.clear()
                    field.send_keys(injection_string)
                    
                    # Enviar formulario
                    FormHelper.submit_form(driver)
                    
                    # Verificar que no se ejecutó la inyección
                    assert "error" in driver.page_source.lower(), f"Posible vulnerabilidad SQL en campo {field_name}"
                    
                except Exception as e:
                    print(f"Error probando inyección SQL en {field_name}: {e}")
    
    @staticmethod
    def test_xss_vulnerability(driver, form_fields):
        """Probar vulnerabilidad XSS en formulario"""
        xss_strings = TestDataGenerator.generate_xss_strings()
        
        for xss_string in xss_strings:
            for field_name in form_fields:
                try:
                    field = driver.find_element(By.NAME, field_name)
                    field.clear()
                    field.send_keys(xss_string)
                    
                    # Enviar formulario
                    FormHelper.submit_form(driver)
                    
                    # Verificar que el script no se ejecutó
                    assert xss_string not in driver.page_source, f"Posible vulnerabilidad XSS en campo {field_name}"
                    
                except Exception as e:
                    print(f"Error probando XSS en {field_name}: {e}")

class PerformanceHelper:
    """Helper para tests de rendimiento"""
    
    @staticmethod
    def measure_page_load_time(driver, url):
        """Medir tiempo de carga de página"""
        start_time = time.time()
        driver.get(url)
        NavigationHelper.wait_for_page_load(driver)
        end_time = time.time()
        
        return end_time - start_time
    
    @staticmethod
    def measure_element_load_time(driver, locator):
        """Medir tiempo de carga de elemento"""
        start_time = time.time()
        WaitHelper.wait_for_element_to_be_clickable(driver, locator)
        end_time = time.time()
        
        return end_time - start_time
    
    @staticmethod
    def check_page_size(driver):
        """Verificar tamaño de página"""
        page_source = driver.page_source
        return len(page_source.encode('utf-8'))

class ReportHelper:
    """Helper para generar reportes"""
    
    @staticmethod
    def generate_test_report(test_results, filename="test_report.html"):
        """Generar reporte HTML de tests"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .passed { color: green; }
                .failed { color: red; }
                .summary { background: #f0f0f0; padding: 10px; margin: 10px 0; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Test Execution Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total Tests: {total}</p>
                <p class="passed">Passed: {passed}</p>
                <p class="failed">Failed: {failed}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {test_rows}
                </tbody>
            </table>
        </body>
        </html>
        """
        
        # Procesar resultados de tests
        total = len(test_results)
        passed = sum(1 for result in test_results if result.get('status') == 'passed')
        failed = total - passed
        
        test_rows = ""
        for result in test_results:
            status_class = "passed" if result.get('status') == 'passed' else "failed"
            test_rows += f"""
                <tr>
                    <td>{result.get('name', 'Unknown')}</td>
                    <td class="{status_class}">{result.get('status', 'Unknown')}</td>
                    <td>{result.get('duration', 'N/A')}</td>
                    <td>{result.get('details', '')}</td>
                </tr>
            """
        
        html_content = html_content.format(
            total=total,
            passed=passed,
            failed=failed,
            test_rows=test_rows
        )
        
        # Guardar reporte
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
