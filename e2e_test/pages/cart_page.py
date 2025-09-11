"""
Cart Page Object - Página del carrito de compras
Contiene todos los elementos y acciones del carrito
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    """Page Object para la página del carrito"""
    
    # Locators principales
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    CART_TABLE = (By.CSS_SELECTOR, ".table")
    CART_TOTAL = (By.CSS_SELECTOR, ".cart-total")
    
    # Elementos de productos en el carrito
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-price")
    PRODUCT_QUANTITIES = (By.CSS_SELECTOR, ".quantity-input")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-image")
    
    # Botones de acción
    UPDATE_CART_BUTTON = (By.CSS_SELECTOR, "button[name='update_cart']")
    REMOVE_ITEM_BUTTONS = (By.CSS_SELECTOR, ".remove-item")
    CHECKOUT_BUTTON = (By.XPATH, "//a[contains(text(), 'Checkout') or contains(text(), 'Finalizar')]")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//a[contains(text(), 'Continuar') or contains(text(), 'Continue')]")
    
    # Mensajes
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".empty-cart-message")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    # Totales
    SUBTOTAL = (By.CSS_SELECTOR, ".subtotal")
    TOTAL = (By.CSS_SELECTOR, ".total")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/cart"
    
    def navigate_to_cart(self):
        """Navegar a la página del carrito"""
        self.navigate_to(self.url)
        return self
    
    def get_cart_items_count(self):
        """Obtener cantidad de items en el carrito"""
        items = self.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def is_cart_empty(self):
        """Verificar si el carrito está vacío"""
        return self.is_element_present(*self.EMPTY_CART_MESSAGE) or self.get_cart_items_count() == 0
    
    def get_product_names_in_cart(self):
        """Obtener nombres de productos en el carrito"""
        name_elements = self.find_elements(*self.PRODUCT_NAMES)
        return [element.text for element in name_elements]
    
    def get_product_prices_in_cart(self):
        """Obtener precios de productos en el carrito"""
        price_elements = self.find_elements(*self.PRODUCT_PRICES)
        return [element.text for element in price_elements]
    
    def get_product_quantities_in_cart(self):
        """Obtener cantidades de productos en el carrito"""
        quantity_elements = self.find_elements(*self.PRODUCT_QUANTITIES)
        return [element.get_attribute("value") for element in quantity_elements]
    
    def update_product_quantity(self, product_index, new_quantity):
        """Actualizar cantidad de un producto específico"""
        quantity_inputs = self.find_elements(*self.PRODUCT_QUANTITIES)
        if product_index < len(quantity_inputs):
            quantity_input = quantity_inputs[product_index]
            quantity_input.clear()
            quantity_input.send_keys(str(new_quantity))
            self.click_element(*self.UPDATE_CART_BUTTON)
        return self
    
    def remove_product_from_cart(self, product_index):
        """Remover producto del carrito por índice"""
        remove_buttons = self.find_elements(*self.REMOVE_ITEM_BUTTONS)
        if product_index < len(remove_buttons):
            remove_buttons[product_index].click()
        return self
    
    def remove_all_products_from_cart(self):
        """Remover todos los productos del carrito"""
        while not self.is_cart_empty():
            remove_buttons = self.find_elements(*self.REMOVE_ITEM_BUTTONS)
            if remove_buttons:
                remove_buttons[0].click()
                self.wait_for_page_load()
            else:
                break
        return self
    
    def click_checkout_button(self):
        """Hacer click en el botón de checkout"""
        self.click_element(*self.CHECKOUT_BUTTON)
        return self
    
    def click_continue_shopping_button(self):
        """Hacer click en continuar comprando"""
        self.click_element(*self.CONTINUE_SHOPPING_BUTTON)
        return self
    
    def get_cart_subtotal(self):
        """Obtener subtotal del carrito"""
        if self.is_element_present(*self.SUBTOTAL):
            return self.get_element_text(*self.SUBTOTAL)
        return None
    
    def get_cart_total(self):
        """Obtener total del carrito"""
        if self.is_element_present(*self.TOTAL):
            return self.get_element_text(*self.TOTAL)
        return None
    
    def verify_cart_page_loaded(self):
        """Verificar que la página del carrito cargó correctamente"""
        return (self.is_element_present(*self.CART_TABLE) or 
                self.is_element_present(*self.EMPTY_CART_MESSAGE))
    
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
    
    def verify_product_in_cart(self, product_name):
        """Verificar que un producto específico esté en el carrito"""
        product_names = self.get_product_names_in_cart()
        return any(product_name.lower() in name.lower() for name in product_names)
    
    def get_product_details_in_cart(self):
        """Obtener detalles completos de productos en el carrito"""
        products = []
        names = self.get_product_names_in_cart()
        prices = self.get_product_prices_in_cart()
        quantities = self.get_product_quantities_in_cart()
        
        for i in range(len(names)):
            product = {
                "name": names[i] if i < len(names) else "",
                "price": prices[i] if i < len(prices) else "",
                "quantity": quantities[i] if i < len(quantities) else ""
            }
            products.append(product)
        
        return products
    
    def calculate_expected_total(self):
        """Calcular total esperado basado en productos del carrito"""
        products = self.get_product_details_in_cart()
        total = 0
        
        for product in products:
            try:
                # Extraer precio numérico (remover símbolos de moneda)
                price_text = product["price"].replace("$", "").replace(",", "")
                price = float(price_text)
                quantity = int(product["quantity"])
                total += price * quantity
            except (ValueError, TypeError):
                continue
        
        return total
    
    def verify_cart_calculations(self):
        """Verificar que los cálculos del carrito sean correctos"""
        expected_total = self.calculate_expected_total()
        displayed_total_text = self.get_cart_total()
        
        if displayed_total_text:
            try:
                displayed_total = float(displayed_total_text.replace("$", "").replace(",", ""))
                return abs(expected_total - displayed_total) < 0.01  # Tolerancia para decimales
            except (ValueError, TypeError):
                return False
        
        return False
    
    def test_quantity_update_validation(self):
        """Probar validación de actualización de cantidades"""
        if not self.is_cart_empty():
            # Probar cantidad negativa
            self.update_product_quantity(0, -1)
            negative_quantity_error = self.get_error_message() is not None
            
            # Probar cantidad cero
            self.update_product_quantity(0, 0)
            zero_quantity_behavior = self.get_cart_items_count()
            
            # Probar cantidad muy grande
            self.update_product_quantity(0, 999999)
            large_quantity_error = self.get_error_message() is not None
            
            return {
                "negative_quantity_handled": negative_quantity_error,
                "zero_quantity_items_after": zero_quantity_behavior,
                "large_quantity_handled": large_quantity_error
            }
        
        return None
    
    def verify_cart_persistence(self):
        """Verificar que el carrito persista entre sesiones"""
        initial_cart_count = self.get_cart_items_count()
        
        # Navegar a otra página y regresar
        self.navigate_to("/")
        self.navigate_to_cart()
        
        final_cart_count = self.get_cart_items_count()
        
        return initial_cart_count == final_cart_count
    
    def verify_responsive_design(self):
        """Verificar diseño responsivo del carrito"""
        # Probar en diferentes tamaños de pantalla
        desktop_visible = True
        mobile_visible = True
        
        # Modo desktop
        self.driver.set_window_size(1920, 1080)
        desktop_visible = self.verify_cart_page_loaded()
        
        # Modo mobile
        self.driver.set_window_size(375, 667)
        mobile_visible = self.verify_cart_page_loaded()
        
        # Restaurar tamaño original
        self.driver.set_window_size(1920, 1080)
        
        return {
            "desktop_responsive": desktop_visible,
            "mobile_responsive": mobile_visible
        }
    
    def is_checkout_button_enabled(self):
        """Verificar si el botón de checkout está habilitado"""
        if self.is_element_present(*self.CHECKOUT_BUTTON):
            button = self.find_element(*self.CHECKOUT_BUTTON)
            return button.is_enabled()
        return False
    
    def verify_cart_security(self):
        """Verificar aspectos básicos de seguridad del carrito"""
        security_results = {}
        
        # Verificar que no se puedan inyectar scripts en cantidades
        if not self.is_cart_empty():
            malicious_quantity = "<script>alert('XSS')</script>"
            self.update_product_quantity(0, malicious_quantity)
            security_results["xss_quantity_protected"] = self.get_error_message() is not None
        
        return security_results
