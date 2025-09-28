"""
Home Page Object - Página principal del ecommerce
Contiene todos los elementos y acciones de la página de inicio
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    """Page Object para la página de inicio"""
    
    # Locators (selectores)
    NAVBAR_BRAND = (By.CLASS_NAME, "navbar-brand")
    NAVBAR_LINKS = (By.CSS_SELECTOR, ".navbar-nav .nav-link")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Iniciar Sesión')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(), 'Registrarse')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(), 'Cerrar Sesión')]")
    CART_LINK = (By.XPATH, "//a[contains(@href, 'cart')]")
    SEARCH_FORM = (By.NAME, "searched")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Productos
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".card")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".card-title")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".card-text")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".card-img-top")
    PRODUCT_LINKS = (By.CSS_SELECTOR, ".card-body a")
    
    # Categorías
    CATEGORIES_DROPDOWN = (By.XPATH, "//a[contains(text(), 'Categorías')]")
    CATEGORY_LINKS = (By.CSS_SELECTOR, ".dropdown-menu a")
    
    # Footer
    FOOTER = (By.TAG_NAME, "footer")
    
    # Mensajes
    MESSAGES = (By.CSS_SELECTOR, ".alert")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    # Admin (solo para superusuarios)
    ORDERS_DROPDOWN = (By.XPATH, "//a[contains(text(), 'Pedidos')]")
    SHIPPED_ORDERS = (By.XPATH, "//a[contains(text(), 'Pedidos enviados')]")
    NOT_SHIPPED_ORDERS = (By.XPATH, "//a[contains(text(), 'Pedidos no enviados')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/"
    
    def navigate_to_home(self):
        """Navegar a la página de inicio"""
        self.navigate_to(self.url)
        return self
    
    def get_page_title(self):
        """Obtener título de la página"""
        return self.driver.title
    
    def click_login_link(self):
        """Hacer click en el enlace de login"""
        self.click_element(*self.LOGIN_LINK)
        return self
    
    def click_register_link(self):
        """Hacer click en el enlace de registro"""
        self.click_element(*self.REGISTER_LINK)
        return self
    
    def click_logout_link(self):
        """Hacer click en el enlace de logout"""
        self.click_element(*self.LOGOUT_LINK)
        return self
    
    def click_cart_link(self):
        """Hacer click en el enlace del carrito"""
        self.click_element(*self.CART_LINK)
        return self
    
    def search_product(self, search_term):
        """Buscar producto"""
        self.type_text(*self.SEARCH_FORM, search_term)
        self.click_element(*self.SEARCH_BUTTON)
        return self
    
    def get_product_count(self):
        """Obtener cantidad de productos en la página"""
        products = self.find_elements(*self.PRODUCT_CARDS)
        return len(products)
    
    def get_product_titles(self):
        """Obtener títulos de todos los productos"""
        title_elements = self.find_elements(*self.PRODUCT_TITLES)
        return [element.text for element in title_elements]
    
    def get_product_prices(self):
        """Obtener precios de todos los productos"""
        price_elements = self.find_elements(*self.PRODUCT_PRICES)
        return [element.text for element in price_elements]
    
    def click_product_by_index(self, index):
        """Hacer click en producto por índice"""
        product_links = self.find_elements(*self.PRODUCT_LINKS)
        if index < len(product_links):
            product_links[index].click()
        return self
    
    def click_product_by_name(self, product_name):
        """Hacer click en producto por nombre"""
        product_links = self.find_elements(*self.PRODUCT_LINKS)
        for link in product_links:
            if product_name.lower() in link.text.lower():
                link.click()
                break
        return self
    
    def click_categories_dropdown(self):
        """Hacer click en dropdown de categorías"""
        self.click_element(*self.CATEGORIES_DROPDOWN)
        return self
    
    def get_category_list(self):
        """Obtener lista de categorías"""
        self.click_categories_dropdown()
        category_elements = self.find_elements(*self.CATEGORY_LINKS)
        return [element.text for element in category_elements]
    
    def select_category(self, category_name):
        """Seleccionar categoría específica"""
        self.click_categories_dropdown()
        category_links = self.find_elements(*self.CATEGORY_LINKS)
        for link in category_links:
            if category_name.lower() in link.text.lower():
                link.click()
                break
        return self
    
    def is_user_logged_in(self):
        """Verificar si usuario está logueado"""
        return self.is_element_present(*self.LOGOUT_LINK)
    
    def is_admin_user(self):
        """Verificar si usuario es administrador"""
        return self.is_element_present(*self.ORDERS_DROPDOWN)
    
    def get_success_message(self):
        """Obtener mensaje de éxito"""
        if self.is_element_present(*self.SUCCESS_MESSAGE):
            return self.get_element_text(*self.SUCCESS_MESSAGE)
        return None
    
    def get_error_message(self):
        """Obtener mensaje de error"""
        if self.is_element_present(*self.ERROR_MESSAGE):
            return self.get_element_text(*self.ERROR_MESSAGE)
        return None
    
    def click_orders_dropdown(self):
        """Hacer click en dropdown de pedidos (admin)"""
        self.click_element(*self.ORDERS_DROPDOWN)
        return self
    
    def click_shipped_orders(self):
        """Hacer click en pedidos enviados (admin)"""
        self.click_orders_dropdown()
        self.click_element(*self.SHIPPED_ORDERS)
        return self
    
    def click_not_shipped_orders(self):
        """Hacer click en pedidos no enviados (admin)"""
        self.click_orders_dropdown()
        self.click_element(*self.NOT_SHIPPED_ORDERS)
        return self
    
    def verify_home_page_loaded(self):
        """Verificar que la página de inicio cargó correctamente"""
        self.wait_for_element(*self.NAVBAR_BRAND)
        return self.is_element_present(*self.NAVBAR_BRAND)
    
    def get_navbar_links(self):
        """Obtener todos los enlaces del navbar"""
        link_elements = self.find_elements(*self.NAVBAR_LINKS)
        return [element.text for element in link_elements]
    
    def verify_responsive_design(self):
        """Verificar diseño responsivo básico"""
        # Cambiar tamaño de ventana para probar responsividad
        self.driver.set_window_size(375, 667)  # iPhone size
        mobile_responsive = self.is_element_visible(*self.NAVBAR_BRAND)
        
        self.driver.set_window_size(1920, 1080)  # Desktop size
        desktop_responsive = self.is_element_visible(*self.NAVBAR_BRAND)
        
        return mobile_responsive and desktop_responsive
    
    def count_products_on_page(self):
        """Contar productos en la página actual"""
        return len(self.find_elements(*self.PRODUCT_CARDS))
    
    def get_first_product_info(self):
        """Obtener información del primer producto"""
        if self.count_products_on_page() > 0:
            title = self.find_elements(*self.PRODUCT_TITLES)[0].text
            price = self.find_elements(*self.PRODUCT_PRICES)[0].text
            return {"title": title, "price": price}
        return None
    
    def verify_all_images_loaded(self):
        """Verificar que todas las imágenes de productos cargaron"""
        images = self.find_elements(*self.PRODUCT_IMAGES)
        for image in images:
            if not image.get_attribute("src"):
                return False
        return True
