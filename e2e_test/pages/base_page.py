"""
Base Page - Clase padre para todos los Page Objects
Implementa el patrón Page Object Model (POM) para mantener código limpio y reutilizable
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    """Clase base para todos los Page Objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
        self.base_url = "http://127.0.0.1:8001"
    
    def navigate_to(self, url):
        """Navegar a una URL específica"""
        full_url = self.base_url + url if not url.startswith('http') else url
        self.driver.get(full_url)
    
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Obtener título de la página"""
        return self.driver.title
    
    def find_element(self, by, value):
        """Encontrar elemento con manejo de errores"""
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            raise NoSuchElementException(f"Element not found: {by}={value}")
    
    def find_elements(self, by, value):
        """Encontrar múltiples elementos"""
        return self.driver.find_elements(by, value)
    
    def wait_for_element(self, by, value, timeout=10):
        """Esperar por elemento con timeout personalizado"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))
    
    def wait_for_clickable_element(self, by, value, timeout=10):
        """Esperar por elemento clickeable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def wait_for_element_to_disappear(self, by, value, timeout=10):
        """Esperar que un elemento desaparezca"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located((by, value)))
    
    def click_element(self, by, value):
        """Hacer click en elemento con espera"""
        element = self.wait_for_clickable_element(by, value)
        element.click()
        return element
    
    def type_text(self, by, value, text):
        """Escribir texto en elemento"""
        element = self.wait_for_element(by, value)
        element.clear()
        element.send_keys(text)
        return element
    
    def get_element_text(self, by, value):
        """Obtener texto de elemento"""
        element = self.wait_for_element(by, value)
        return element.text
    
    def get_element_attribute(self, by, value, attribute):
        """Obtener atributo de elemento"""
        element = self.wait_for_element(by, value)
        return element.get_attribute(attribute)
    
    def is_element_visible(self, by, value, timeout=5):
        """Verificar si elemento es visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, by, value):
        """Verificar si elemento está presente en DOM"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def scroll_to_element(self, by, value):
        """Hacer scroll hasta elemento"""
        element = self.wait_for_element(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element
    
    def hover_over_element(self, by, value):
        """Hacer hover sobre elemento"""
        element = self.wait_for_element(by, value)
        self.actions.move_to_element(element).perform()
        return element
    
    def select_dropdown_by_text(self, by, value, text):
        """Seleccionar opción en dropdown por texto"""
        element = self.wait_for_element(by, value)
        select = Select(element)
        select.select_by_visible_text(text)
        return element
    
    def select_dropdown_by_value(self, by, value, option_value):
        """Seleccionar opción en dropdown por valor"""
        element = self.wait_for_element(by, value)
        select = Select(element)
        select.select_by_value(option_value)
        return element
    
    def take_screenshot(self, name):
        """Tomar screenshot"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{name}_{timestamp}.png"
        screenshot_path = f"e2e_test/reports/screenshots/{screenshot_name}"
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path
    
    def refresh_page(self):
        """Refrescar página"""
        self.driver.refresh()
    
    def go_back(self):
        """Navegar hacia atrás"""
        self.driver.back()
    
    def go_forward(self):
        """Navegar hacia adelante"""
        self.driver.forward()
    
    def switch_to_window(self, window_handle):
        """Cambiar a ventana específica"""
        self.driver.switch_to.window(window_handle)
    
    def get_window_handles(self):
        """Obtener todas las ventanas/tabs"""
        return self.driver.window_handles
    
    def execute_javascript(self, script, *args):
        """Ejecutar JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def wait_for_page_load(self, timeout=30):
        """Esperar que la página cargue completamente"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def get_alert_text(self):
        """Obtener texto de alerta JavaScript"""
        alert = self.driver.switch_to.alert
        return alert.text
    
    def accept_alert(self):
        """Aceptar alerta JavaScript"""
        alert = self.driver.switch_to.alert
        alert.accept()
    
    def dismiss_alert(self):
        """Cancelar alerta JavaScript"""
        alert = self.driver.switch_to.alert
        alert.dismiss()
    
    def wait_for_text_in_element(self, by, value, text, timeout=10):
        """Esperar por texto específico en elemento"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.text_to_be_present_in_element((by, value), text))
    
    def wait_for_url_contains(self, url_part, timeout=10):
        """Esperar que URL contenga texto específico"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(url_part))
    
    def get_current_timestamp(self):
        """Obtener timestamp actual"""
        return int(time.time())
    
    def wait_and_retry(self, function, max_attempts=3, wait_time=1):
        """Reintentar función hasta que sea exitosa"""
        for attempt in range(max_attempts):
            try:
                return function()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(wait_time)
    
    def get_page_source(self):
        """Obtener código fuente de la página"""
        return self.driver.page_source
    
    def clear_browser_cache(self):
        """Limpiar cache del navegador"""
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
