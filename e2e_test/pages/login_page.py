"""
Login Page Object - Página de inicio de sesión
Contiene todos los elementos y acciones de la página de login
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    """Page Object para la página de login"""
    
    # Locators
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_FORM = (By.TAG_NAME, "form")
    
    # Mensajes
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    # Enlaces
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Registrarse')]")
    HOME_LINK = (By.CLASS_NAME, "navbar-brand")
    
    # Título de la página
    PAGE_TITLE = (By.TAG_NAME, "h1")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/login"
    
    def navigate_to_login(self):
        """Navegar a la página de login"""
        self.navigate_to(self.url)
        return self
    
    def enter_username(self, username):
        """Introducir nombre de usuario"""
        self.type_text(*self.USERNAME_FIELD, username)
        return self
    
    def enter_password(self, password):
        """Introducir contraseña"""
        self.type_text(*self.PASSWORD_FIELD, password)
        return self
    
    def click_login_button(self):
        """Hacer click en el botón de login"""
        self.click_element(*self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """Proceso completo de login"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self):
        """Obtener mensaje de error"""
        if self.is_element_present(*self.ERROR_MESSAGE):
            return self.get_element_text(*self.ERROR_MESSAGE)
        return None
    
    def get_success_message(self):
        """Obtener mensaje de éxito"""
        if self.is_element_present(*self.SUCCESS_MESSAGE):
            return self.get_element_text(*self.SUCCESS_MESSAGE)
        return None
    
    def click_register_link(self):
        """Hacer click en el enlace de registro"""
        self.click_element(*self.REGISTER_LINK)
        return self
    
    def verify_login_page_loaded(self):
        """Verificar que la página de login cargó correctamente"""
        return (self.is_element_present(*self.USERNAME_FIELD) and 
                self.is_element_present(*self.PASSWORD_FIELD) and
                self.is_element_present(*self.LOGIN_BUTTON))
    
    def verify_login_form_elements(self):
        """Verificar que todos los elementos del formulario estén presentes"""
        elements_present = {
            "username_field": self.is_element_present(*self.USERNAME_FIELD),
            "password_field": self.is_element_present(*self.PASSWORD_FIELD),
            "login_button": self.is_element_present(*self.LOGIN_BUTTON),
            "form": self.is_element_present(*self.LOGIN_FORM)
        }
        return elements_present
    
    def get_username_placeholder(self):
        """Obtener placeholder del campo username"""
        return self.get_element_attribute(*self.USERNAME_FIELD, "placeholder")
    
    def get_password_placeholder(self):
        """Obtener placeholder del campo password"""
        return self.get_element_attribute(*self.PASSWORD_FIELD, "placeholder")
    
    def clear_login_form(self):
        """Limpiar formulario de login"""
        self.find_element(*self.USERNAME_FIELD).clear()
        self.find_element(*self.PASSWORD_FIELD).clear()
        return self
    
    def is_login_button_enabled(self):
        """Verificar si el botón de login está habilitado"""
        button = self.find_element(*self.LOGIN_BUTTON)
        return button.is_enabled()
    
    def get_page_title_text(self):
        """Obtener texto del título de la página"""
        if self.is_element_present(*self.PAGE_TITLE):
            return self.get_element_text(*self.PAGE_TITLE)
        return None
    
    def verify_spanish_localization(self):
        """Verificar que la página esté en español"""
        spanish_indicators = [
            "Iniciar Sesión" in self.driver.page_source,
            "Nombre de Usuario" in self.driver.page_source or "usuario" in self.get_username_placeholder().lower(),
            "Contraseña" in self.driver.page_source or "contraseña" in self.get_password_placeholder().lower()
        ]
        return all(spanish_indicators)
    
    def attempt_sql_injection(self):
        """Intentar inyección SQL básica (test de seguridad)"""
        malicious_input = "' OR '1'='1"
        self.enter_username(malicious_input)
        self.enter_password(malicious_input)
        self.click_login_button()
        return self
    
    def test_empty_credentials(self):
        """Probar credenciales vacías"""
        self.clear_login_form()
        self.click_login_button()
        return self
    
    def test_invalid_credentials(self):
        """Probar credenciales inválidas"""
        self.enter_username("invalid_user")
        self.enter_password("invalid_password")
        self.click_login_button()
        return self
    
    def verify_password_masking(self):
        """Verificar que la contraseña esté enmascarada"""
        password_field = self.find_element(*self.PASSWORD_FIELD)
        return password_field.get_attribute("type") == "password"
    
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    def verify_redirect_after_login(self):
        """Verificar redirección después del login exitoso"""
        return "/login" not in self.get_current_url()
    
    def test_remember_me_functionality(self):
        """Probar funcionalidad 'recordarme' si existe"""
        remember_checkbox = (By.NAME, "remember")
        if self.is_element_present(*remember_checkbox):
            self.click_element(*remember_checkbox)
            return True
        return False
    
    def verify_form_validation(self):
        """Verificar validación del formulario"""
        validation_results = {}
        
        # Test campo username vacío
        self.clear_login_form()
        self.enter_password("password123")
        self.click_login_button()
        validation_results["empty_username"] = self.get_error_message() is not None
        
        # Test campo password vacío
        self.clear_login_form()
        self.enter_username("testuser")
        self.click_login_button()
        validation_results["empty_password"] = self.get_error_message() is not None
        
        return validation_results
