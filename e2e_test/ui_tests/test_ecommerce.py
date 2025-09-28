"""
Tests de UI para funcionalidad del ecommerce
Incluye tests para navegación, productos, búsqueda, etc.
"""
import pytest
import time
from e2e_test.pages.home_page import HomePage
from e2e_test.pages.cart_page import CartPage
from e2e_test.pages.login_page import LoginPage
from e2e_test.pages.register_page import RegisterPage

class TestEcommerceFunctionality:
    """Suite de tests para funcionalidad del ecommerce"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_home_page_loads_correctly(self, driver):
        """Verificar que la página principal carga correctamente"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        assert home_page.verify_home_page_loaded(), "La página principal no cargó correctamente"
        assert home_page.get_page_title(), "No hay título en la página"
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_navbar_elements_present(self, driver):
        """Verificar que todos los elementos del navbar estén presentes"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        navbar_links = home_page.get_navbar_links()
        assert len(navbar_links) > 0, "No hay enlaces en el navbar"
        
        # Verificar enlaces específicos
        assert home_page.is_element_present(*home_page.LOGIN_LINK), "Enlace de login no presente"
        assert home_page.is_element_present(*home_page.REGISTER_LINK), "Enlace de registro no presente"
        assert home_page.is_element_present(*home_page.CART_LINK), "Enlace de carrito no presente"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_products_display_correctly(self, driver):
        """Verificar que los productos se muestren correctamente"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        product_count = home_page.get_product_count()
        assert product_count > 0, "No hay productos en la página"
        
        product_titles = home_page.get_product_titles()
        assert len(product_titles) > 0, "No hay títulos de productos"
        
        # Verificar que los títulos no estén vacíos
        for title in product_titles:
            assert title.strip(), "Hay títulos de productos vacíos"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_product_images_load(self, driver):
        """Verificar que las imágenes de productos cargan correctamente"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        assert home_page.verify_all_images_loaded(), "No todas las imágenes cargaron correctamente"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_search_functionality(self, driver):
        """Probar funcionalidad de búsqueda"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Obtener un producto para buscar
        product_info = home_page.get_first_product_info()
        if product_info:
            search_term = product_info["title"].split()[0]  # Primera palabra del título
            
            home_page.search_product(search_term)
            
            # Verificar que se realizó la búsqueda
            current_url = home_page.get_current_url()
            assert "search" in current_url, "No se redirigió a página de búsqueda"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_categories_dropdown(self, driver):
        """Probar dropdown de categorías"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Verificar que el dropdown existe
        assert home_page.is_element_present(*home_page.CATEGORIES_DROPDOWN), "Dropdown de categorías no presente"
        
        # Obtener categorías
        categories = home_page.get_category_list()
        assert len(categories) > 0, "No hay categorías disponibles"
        
        # Probar selección de una categoría
        if categories:
            home_page.select_category(categories[0])
            
            # Verificar que se navegó a la categoría
            current_url = home_page.get_current_url()
            assert "category" in current_url, "No se navegó a la página de categoría"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_product_detail_navigation(self, driver):
        """Probar navegación a detalle de producto"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        if home_page.get_product_count() > 0:
            home_page.click_product_by_index(0)
            
            # Verificar que se navegó a detalle del producto
            current_url = home_page.get_current_url()
            assert "product" in current_url, "No se navegó a página de detalle del producto"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_cart_navigation(self, driver):
        """Probar navegación al carrito"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        home_page.click_cart_link()
        
        # Verificar que se navegó al carrito
        current_url = home_page.get_current_url()
        assert "cart" in current_url, "No se navegó al carrito"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_cart_page_loads_correctly(self, driver):
        """Verificar que la página del carrito carga correctamente"""
        cart_page = CartPage(driver)
        cart_page.navigate_to_cart()
        
        assert cart_page.verify_cart_page_loaded(), "La página del carrito no cargó correctamente"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_empty_cart_display(self, driver):
        """Verificar que el carrito vacío se muestre correctamente"""
        cart_page = CartPage(driver)
        cart_page.navigate_to_cart()
        
        # Si el carrito está vacío, debería mostrar mensaje apropiado
        if cart_page.is_cart_empty():
            assert cart_page.is_element_present(*cart_page.EMPTY_CART_MESSAGE), "No se muestra mensaje de carrito vacío"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_responsive_design(self, driver):
        """Probar diseño responsivo"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        assert home_page.verify_responsive_design(), "El diseño no es responsivo"
        
        # Probar carrito responsivo
        cart_page = CartPage(driver)
        cart_page.navigate_to_cart()
        
        responsive_results = cart_page.verify_responsive_design()
        assert responsive_results["desktop_responsive"], "Carrito no es responsivo en desktop"
        assert responsive_results["mobile_responsive"], "Carrito no es responsivo en mobile"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_messages_display(self, driver):
        """Probar que los mensajes del sistema se muestren correctamente"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Ir a login con credenciales incorrectas para generar mensaje
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login("usuario_inexistente", "contraseña_incorrecta")
        
        # Verificar que se muestra mensaje de error
        error_message = login_page.get_error_message()
        assert error_message is not None, "No se muestra mensaje de error"
        assert len(error_message) > 0, "Mensaje de error está vacío"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_spanish_localization(self, driver):
        """Verificar que la aplicación esté en español"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Verificar términos en español en la página principal
        page_source = home_page.get_page_source()
        spanish_terms = ["Iniciar Sesión", "Registrarse", "Carrito", "Categorías"]
        
        for term in spanish_terms:
            assert term in page_source, f"Término '{term}' no encontrado en español"
        
        # Verificar en páginas de autenticación
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        assert login_page.verify_spanish_localization(), "Página de login no está en español"
        
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        assert register_page.verify_spanish_localization(), "Página de registro no está en español"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_admin_functionality_visibility(self, driver, admin_user_data):
        """Verificar que la funcionalidad de admin sea visible solo para administradores"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Verificar que no se muestra dropdown de pedidos para usuario no logueado
        assert not home_page.is_admin_user(), "Funcionalidad de admin visible sin autenticación"
        
        # Intentar login como admin (si existe)
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login(admin_user_data["username"], admin_user_data["password"])
        
        # Verificar si es admin después del login
        home_page.navigate_to_home()
        if home_page.is_admin_user():
            assert home_page.is_element_present(*home_page.ORDERS_DROPDOWN), "Dropdown de pedidos no visible para admin"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_page_titles_and_meta(self, driver):
        """Verificar títulos de página y metadatos básicos"""
        pages_to_test = [
            ("home", "/"),
            ("login", "/login"),
            ("register", "/register"),
            ("cart", "/cart")
        ]
        
        home_page = HomePage(driver)
        
        for page_name, url in pages_to_test:
            home_page.navigate_to(url)
            title = home_page.get_page_title()
            assert title is not None, f"No hay título en página {page_name}"
            assert len(title) > 0, f"Título vacío en página {page_name}"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_navigation_breadcrumbs(self, driver):
        """Probar navegación y breadcrumbs si existen"""
        home_page = HomePage(driver)
        
        # Navegar a diferentes páginas y verificar que se puede volver
        home_page.navigate_to_home()
        original_url = home_page.get_current_url()
        
        # Ir a login
        home_page.click_login_link()
        assert "login" in home_page.get_current_url(), "No se navegó a login"
        
        # Volver usando el navegador
        home_page.go_back()
        assert home_page.get_current_url() == original_url, "No se puede volver a la página anterior"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_form_error_handling(self, driver):
        """Probar manejo de errores en formularios"""
        # Test formulario de login
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        
        # Campos vacíos
        login_page.test_empty_credentials()
        assert not login_page.verify_redirect_after_login(), "Se redirigió con campos vacíos"
        
        # Credenciales incorrectas
        login_page.test_invalid_credentials()
        error_message = login_page.get_error_message()
        assert error_message is not None, "No se mostró mensaje de error para credenciales incorrectas"
        
        # Test formulario de registro
        register_page = RegisterPage(driver)
        register_page.navigate_to_register()
        
        # Campos vacíos
        register_page.test_empty_required_fields()
        assert not register_page.verify_redirect_after_registration(), "Se redirigió con campos vacíos"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_accessibility_basics(self, driver):
        """Probar aspectos básicos de accesibilidad"""
        home_page = HomePage(driver)
        home_page.navigate_to_home()
        
        # Verificar que las imágenes tienen atributos alt
        images = home_page.find_elements(*home_page.PRODUCT_IMAGES)
        for image in images:
            alt_text = image.get_attribute("alt")
            assert alt_text is not None, "Imagen sin atributo alt"
        
        # Verificar que los botones tienen texto o labels
        buttons = home_page.find_elements("tag name", "button")
        for button in buttons:
            button_text = button.text or button.get_attribute("aria-label")
            assert button_text, "Botón sin texto o aria-label"
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_performance_basic(self, driver):
        """Probar aspectos básicos de rendimiento"""
        home_page = HomePage(driver)
        
        # Medir tiempo de carga de página principal
        start_time = time.time()
        home_page.navigate_to_home()
        home_page.wait_for_page_load()
        load_time = time.time() - start_time
        
        # La página debería cargar en menos de 10 segundos
        assert load_time < 10, f"Página principal tarda demasiado en cargar: {load_time:.2f}s"
        
        # Verificar que hay productos visibles
        product_count = home_page.get_product_count()
        assert product_count > 0, "No hay productos visibles después de la carga"
