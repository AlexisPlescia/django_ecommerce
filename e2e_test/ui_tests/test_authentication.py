"""
Tests de UI para funcionalidad de autenticación
Incluye tests para login, registro y logout
"""
import pytest
import time
from e2e_test.pages.home_page import HomePage
from e2e_test.pages.login_page import LoginPage
from e2e_test.pages.register_page import RegisterPage

class TestAuthentication:
    """Suite de tests para autenticación"""
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_page_loads_correctly(self, driver):
        """Verificar que la página de login carga correctamente"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        assert login_page.verify_login_page_loaded(), "La página de login no cargó correctamente"
        assert login_page.verify_spanish_localization(), "La página no está en español"
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_register_page_loads_correctly(self, driver):
        """Verificar que la página de registro carga correctamente"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        assert register_page.verify_register_page_loaded(), "La página de registro no cargó correctamente"
        assert register_page.verify_spanish_localization(), "La página no está en español"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_successful_user_registration(self, driver, test_user_data):
        """Probar registro exitoso de usuario"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        # Registrar usuario
        register_page.register_user(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        # Verificar redirección exitosa
        assert register_page.verify_redirect_after_registration(), "No se redirigió después del registro"
        
        # Verificar que el usuario está logueado
        home_page = HomePage(driver)
        assert home_page.is_user_logged_in(), "El usuario no está logueado después del registro"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_successful_user_login(self, driver, test_user_data):
        """Probar login exitoso de usuario"""
        # Primero registrar el usuario
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        register_page.register_user(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        # Hacer logout
        home_page = HomePage(driver)
        home_page.click_logout_link()
        
        # Hacer login
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login(test_user_data["username"], test_user_data["password"])
        
        # Verificar login exitoso
        assert login_page.verify_redirect_after_login(), "No se redirigió después del login"
        assert home_page.is_user_logged_in(), "El usuario no está logueado"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_login_with_invalid_credentials(self, driver):
        """Probar login con credenciales inválidas"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.login("usuario_inexistente", "contraseña_incorrecta")
        
        # Verificar que no se redirigió
        assert not login_page.verify_redirect_after_login(), "Se redirigió con credenciales inválidas"
        
        # Verificar mensaje de error
        error_message = login_page.get_error_message()
        assert error_message is not None, "No se mostró mensaje de error"
        assert "error" in error_message.lower(), "El mensaje de error no es apropiado"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_login_with_empty_fields(self, driver):
        """Probar login con campos vacíos"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.test_empty_credentials()
        
        # Verificar que no se redirigió
        assert not login_page.verify_redirect_after_login(), "Se redirigió con campos vacíos"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_register_with_password_mismatch(self, driver, test_user_data):
        """Probar registro con contraseñas que no coinciden"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        register_page.test_password_mismatch(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            password1=test_user_data["password"],
            password2="contraseña_diferente"
        )
        
        # Verificar que no se redirigió
        assert not register_page.verify_redirect_after_registration(), "Se redirigió con contraseñas diferentes"
        
        # Verificar mensaje de error
        error_message = register_page.get_error_message()
        assert error_message is not None, "No se mostró mensaje de error"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_register_with_weak_password(self, driver, test_user_data):
        """Probar registro con contraseña débil"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        register_page.test_weak_password(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            weak_password="123"
        )
        
        # Verificar que no se redirigió
        assert not register_page.verify_redirect_after_registration(), "Se redirigió con contraseña débil"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_register_with_invalid_email(self, driver, test_user_data):
        """Probar registro con email inválido"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        register_page.test_invalid_email(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            invalid_email="email_invalido",
            password=test_user_data["password"]
        )
        
        # Verificar que no se redirigió
        assert not register_page.verify_redirect_after_registration(), "Se redirigió con email inválido"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_register_with_existing_username(self, driver, test_user_data):
        """Probar registro con username que ya existe"""
        register_page = RegisterPage(driver)
        
        # Primero registrar un usuario
        register_page.navigate_to_register()
        register_page.register_user(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        # Hacer logout
        home_page = HomePage(driver)
        home_page.click_logout_link()
        
        # Intentar registrar con el mismo username
        register_page.navigate_to_register()
        register_page.test_username_already_exists(
            existing_username=test_user_data["username"],
            first_name="Otro",
            last_name="Usuario",
            email="otro@example.com",
            password=test_user_data["password"]
        )
        
        # Verificar que no se redirigió
        assert not register_page.verify_redirect_after_registration(), "Se redirigió con username existente"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_logout_functionality(self, driver, test_user_data):
        """Probar funcionalidad de logout"""
        # Primero registrar y loguear usuario
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        register_page.register_user(
            username=test_user_data["username"],
            first_name=test_user_data["first_name"],
            last_name=test_user_data["last_name"],
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        
        # Verificar que está logueado
        home_page = HomePage(driver)
        assert home_page.is_user_logged_in(), "El usuario no está logueado"
        
        # Hacer logout
        home_page.click_logout_link()
        
        # Verificar que ya no está logueado
        assert not home_page.is_user_logged_in(), "El usuario sigue logueado después del logout"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_password_masking(self, driver):
        """Verificar que las contraseñas estén enmascaradas"""
        # Test en login
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        assert login_page.verify_password_masking(), "La contraseña no está enmascarada en login"
        
        # Test en registro
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        assert register_page.verify_password_masking(), "Las contraseñas no están enmascaradas en registro"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_form_validation_messages(self, driver):
        """Verificar mensajes de validación de formularios"""
        # Test validación en login
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        validation_results = login_page.verify_form_validation()
        
        assert validation_results["empty_username"], "No se valida username vacío"
        assert validation_results["empty_password"], "No se valida contraseña vacía"
        
        # Test validación en registro
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        validation_results = register_page.verify_form_validation_messages()
        
        assert validation_results["empty_fields"], "No se validan campos vacíos en registro"
        assert validation_results["password_mismatch"], "No se valida coincidencia de contraseñas"
    
    @pytest.mark.regression
    @pytest.mark.auth
    def test_sql_injection_protection(self, driver):
        """Probar protección contra inyección SQL"""
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        login_page.attempt_sql_injection()
        
        # Verificar que no se redirigió (no se logueó)
        assert not login_page.verify_redirect_after_login(), "Vulnerable a inyección SQL"
        
        # Verificar que hay mensaje de error
        error_message = login_page.get_error_message()
        assert error_message is not None, "No se mostró mensaje de error para inyección SQL"
    
    @pytest.mark.regression
    @pytest.mark.auth 
    def test_xss_protection_in_registration(self, driver):
        """Probar protección contra XSS en registro"""
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        register_page.test_security_xss_attempt()
        
        # Verificar que no hay scripts ejecutándose
        page_source = register_page.get_page_source()
        assert "<script>" not in page_source, "Posible vulnerabilidad XSS"
    
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_navigation_between_auth_pages(self, driver):
        """Probar navegación entre páginas de autenticación"""
        # Ir a login
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        # Ir a registro desde login
        login_page.click_register_link()
        register_page = RegisterPage(driver)
        assert register_page.verify_register_page_loaded(), "No se navegó correctamente a registro"
        
        # Ir a login desde registro
        register_page.click_login_link()
        assert login_page.verify_login_page_loaded(), "No se navegó correctamente a login"
