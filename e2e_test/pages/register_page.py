"""
Register Page Object - Página de registro de usuarios
Contiene todos los elementos y acciones de la página de registro
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegisterPage(BasePage):
    """Page Object para la página de registro"""
    
    # Locators de los campos del formulario
    USERNAME_FIELD = (By.NAME, "username")
    FIRST_NAME_FIELD = (By.NAME, "first_name")
    LAST_NAME_FIELD = (By.NAME, "last_name")
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD1_FIELD = (By.NAME, "password1")
    PASSWORD2_FIELD = (By.NAME, "password2")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Formulario
    REGISTER_FORM = (By.TAG_NAME, "form")
    
    # Mensajes
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    # Mensajes de ayuda
    USERNAME_HELP_TEXT = (By.CSS_SELECTOR, "small:contains('Requerido')")
    PASSWORD_HELP_TEXT = (By.CSS_SELECTOR, "ul.form-text")
    
    # Enlaces
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Iniciar Sesión')]")
    HOME_LINK = (By.CLASS_NAME, "navbar-brand")
    
    # Título de la página
    PAGE_TITLE = (By.TAG_NAME, "h1")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/register"
    
    def navigate_to_register(self):
        """Navegar a la página de registro"""
        self.navigate_to(self.url)
        return self
    
    def enter_username(self, username):
        """Introducir nombre de usuario"""
        self.type_text(*self.USERNAME_FIELD, username)
        return self
    
    def enter_first_name(self, first_name):
        """Introducir nombre"""
        self.type_text(*self.FIRST_NAME_FIELD, first_name)
        return self
    
    def enter_last_name(self, last_name):
        """Introducir apellido"""
        self.type_text(*self.LAST_NAME_FIELD, last_name)
        return self
    
    def enter_email(self, email):
        """Introducir email"""
        self.type_text(*self.EMAIL_FIELD, email)
        return self
    
    def enter_password1(self, password):
        """Introducir contraseña"""
        self.type_text(*self.PASSWORD1_FIELD, password)
        return self
    
    def enter_password2(self, password):
        """Confirmar contraseña"""
        self.type_text(*self.PASSWORD2_FIELD, password)
        return self
    
    def click_register_button(self):
        """Hacer click en el botón de registro"""
        self.click_element(*self.REGISTER_BUTTON)
        return self
    
    def register_user(self, username, first_name, last_name, email, password):
        """Proceso completo de registro"""
        self.enter_username(username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password1(password)
        self.enter_password2(password)
        self.click_register_button()
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
    
    def verify_register_page_loaded(self):
        """Verificar que la página de registro cargó correctamente"""
        required_fields = [
            self.USERNAME_FIELD,
            self.FIRST_NAME_FIELD,
            self.LAST_NAME_FIELD,
            self.EMAIL_FIELD,
            self.PASSWORD1_FIELD,
            self.PASSWORD2_FIELD,
            self.REGISTER_BUTTON
        ]
        
        return all(self.is_element_present(*field) for field in required_fields)
    
    def verify_all_form_fields_present(self):
        """Verificar que todos los campos del formulario estén presentes"""
        fields_status = {
            "username": self.is_element_present(*self.USERNAME_FIELD),
            "first_name": self.is_element_present(*self.FIRST_NAME_FIELD),
            "last_name": self.is_element_present(*self.LAST_NAME_FIELD),
            "email": self.is_element_present(*self.EMAIL_FIELD),
            "password1": self.is_element_present(*self.PASSWORD1_FIELD),
            "password2": self.is_element_present(*self.PASSWORD2_FIELD),
            "register_button": self.is_element_present(*self.REGISTER_BUTTON)
        }
        return fields_status
    
    def get_field_placeholder(self, field_locator):
        """Obtener placeholder de un campo específico"""
        return self.get_element_attribute(*field_locator, "placeholder")
    
    def get_all_placeholders(self):
        """Obtener todos los placeholders"""
        return {
            "username": self.get_field_placeholder(self.USERNAME_FIELD),
            "first_name": self.get_field_placeholder(self.FIRST_NAME_FIELD),
            "last_name": self.get_field_placeholder(self.LAST_NAME_FIELD),
            "email": self.get_field_placeholder(self.EMAIL_FIELD),
            "password1": self.get_field_placeholder(self.PASSWORD1_FIELD),
            "password2": self.get_field_placeholder(self.PASSWORD2_FIELD)
        }
    
    def verify_spanish_localization(self):
        """Verificar que la página esté en español"""
        placeholders = self.get_all_placeholders()
        spanish_indicators = [
            "Nombre de Usuario" in placeholders["username"] or "usuario" in placeholders["username"].lower(),
            "Nombre" in placeholders["first_name"] or "nombre" in placeholders["first_name"].lower(),
            "Apellido" in placeholders["last_name"] or "apellido" in placeholders["last_name"].lower(),
            "Correo" in placeholders["email"] or "email" in placeholders["email"].lower(),
            "Contraseña" in placeholders["password1"] or "contraseña" in placeholders["password1"].lower(),
            "Confirmar" in placeholders["password2"] or "confirmar" in placeholders["password2"].lower()
        ]
        return all(spanish_indicators)
    
    def clear_all_fields(self):
        """Limpiar todos los campos del formulario"""
        fields = [
            self.USERNAME_FIELD,
            self.FIRST_NAME_FIELD,
            self.LAST_NAME_FIELD,
            self.EMAIL_FIELD,
            self.PASSWORD1_FIELD,
            self.PASSWORD2_FIELD
        ]
        
        for field in fields:
            self.find_element(*field).clear()
        return self
    
    def test_password_mismatch(self, username, first_name, last_name, email, password1, password2):
        """Probar contraseñas que no coinciden"""
        self.enter_username(username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password1(password1)
        self.enter_password2(password2)
        self.click_register_button()
        return self
    
    def test_weak_password(self, username, first_name, last_name, email, weak_password):
        """Probar contraseña débil"""
        self.enter_username(username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password1(weak_password)
        self.enter_password2(weak_password)
        self.click_register_button()
        return self
    
    def test_invalid_email(self, username, first_name, last_name, invalid_email, password):
        """Probar email inválido"""
        self.enter_username(username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(invalid_email)
        self.enter_password1(password)
        self.enter_password2(password)
        self.click_register_button()
        return self
    
    def test_empty_required_fields(self):
        """Probar campos requeridos vacíos"""
        self.clear_all_fields()
        self.click_register_button()
        return self
    
    def test_username_already_exists(self, existing_username, first_name, last_name, email, password):
        """Probar username que ya existe"""
        self.enter_username(existing_username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_password1(password)
        self.enter_password2(password)
        self.click_register_button()
        return self
    
    def verify_password_masking(self):
        """Verificar que las contraseñas estén enmascaradas"""
        password1_field = self.find_element(*self.PASSWORD1_FIELD)
        password2_field = self.find_element(*self.PASSWORD2_FIELD)
        
        return (password1_field.get_attribute("type") == "password" and 
                password2_field.get_attribute("type") == "password")
    
    def get_password_help_text(self):
        """Obtener texto de ayuda para la contraseña"""
        if self.is_element_present(*self.PASSWORD_HELP_TEXT):
            return self.get_element_text(*self.PASSWORD_HELP_TEXT)
        return None
    
    def verify_redirect_after_registration(self):
        """Verificar redirección después del registro exitoso"""
        return "/register" not in self.get_current_url()
    
    def get_current_url(self):
        """Obtener URL actual"""
        return self.driver.current_url
    
    def click_login_link(self):
        """Hacer click en el enlace de login"""
        self.click_element(*self.LOGIN_LINK)
        return self
    
    def verify_form_validation_messages(self):
        """Verificar mensajes de validación del formulario"""
        validation_results = {}
        
        # Test con campos vacíos
        self.clear_all_fields()
        self.click_register_button()
        validation_results["empty_fields"] = self.get_error_message() is not None
        
        # Test con contraseñas diferentes
        self.clear_all_fields()
        self.enter_username("testuser")
        self.enter_first_name("Test")
        self.enter_last_name("User")
        self.enter_email("test@example.com")
        self.enter_password1("password123")
        self.enter_password2("different123")
        self.click_register_button()
        validation_results["password_mismatch"] = self.get_error_message() is not None
        
        return validation_results
    
    def test_security_xss_attempt(self):
        """Probar intento básico de XSS"""
        malicious_script = "<script>alert('XSS')</script>"
        self.enter_username(malicious_script)
        self.enter_first_name(malicious_script)
        self.enter_last_name(malicious_script)
        self.enter_email("test@example.com")
        self.enter_password1("password123")
        self.enter_password2("password123")
        self.click_register_button()
        return self
    
    def verify_character_limits(self):
        """Verificar límites de caracteres en los campos"""
        long_string = "a" * 200  # String muy largo
        
        self.enter_username(long_string)
        self.enter_first_name(long_string)
        self.enter_last_name(long_string)
        self.enter_email(f"{long_string}@example.com")
        
        # Verificar que los campos acepten solo cierta cantidad de caracteres
        username_value = self.get_element_attribute(*self.USERNAME_FIELD, "value")
        first_name_value = self.get_element_attribute(*self.FIRST_NAME_FIELD, "value")
        
        return {
            "username_length": len(username_value),
            "first_name_length": len(first_name_value),
            "username_truncated": len(username_value) < len(long_string),
            "first_name_truncated": len(first_name_value) < len(long_string)
        }
