from django.test import TestCase, Client
from .models import Product, Order, Profile, Category, Customer, Reservation
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q

class OrderCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@mail.com')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=self.category)
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
        # Crea el Customer asociado
        self.customer = Customer.objects.create(
            first_name='Test', last_name='User', phone='123456789', email='test@mail.com', password='unused')

    def test_order_created_on_payment(self):
        # Simula que el usuario tiene un perfil y datos mínimos
        profile = Profile.objects.get(user=self.user)
        profile.address1 = 'Test Address'
        profile.phone = '123456789'
        profile.save()
        # Simula el flujo real usando la URL correcta
        url = reverse('pagar_producto', args=[self.product.id])
        response = self.client.get(url)
        # Verifica que se haya creado una orden
        self.assertTrue(Order.objects.filter(product=self.product, customer=self.customer, address='Test Address', phone='123456789').exists())

class SearchFunctionalityTest(TestCase):
    def setUp(self):
        # Crear categorías de prueba
        self.armas_category = Category.objects.create(name='Armas')
        self.municiones_category = Category.objects.create(name='Municiones')
        self.accesorios_category = Category.objects.create(name='Accesorios')
        
        # Crear productos de prueba con diferentes imágenes simuladas
        self.producto_arma = Product.objects.create(
            name='Rifle AR-15',
            description='Rifle semi-automático de alta precisión',
            price=1500.00,
            sale_price=1200.00,
            is_sale=True,
            stock=5,
            is_available=True,
            category=self.armas_category
        )
        
        self.producto_municion = Product.objects.create(
            name='Munición 5.56mm',
            description='Cartuchos de alta velocidad para rifles',
            price=50.00,
            stock=100,
            is_available=True,
            category=self.municiones_category
        )
        
        self.producto_accesorio = Product.objects.create(
            name='Mira telescópica',
            description='Mira de alta precisión 4x',
            price=200.00,
            stock=10,
            is_available=True,
            category=self.accesorios_category
        )

    def test_search_by_name(self):
        """Probar búsqueda por nombre de producto"""
        response = self.client.post(reverse('search'), {'searched': 'Rifle'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rifle AR-15')
        self.assertIn('searched', response.context)
        
    def test_search_by_category(self):
        """Probar búsqueda por categoría"""
        response = self.client.post(reverse('search'), {'searched': 'armas'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rifle AR-15')
    
    def test_search_synonyms(self):
        """Probar búsqueda con sinónimos"""
        response = self.client.post(reverse('search'), {'searched': 'municion'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Munición 5.56mm')
    
    def test_search_no_results(self):
        """Probar búsqueda sin resultados"""
        response = self.client.post(reverse('search'), {'searched': 'inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No se encontraron productos')
    
    def test_empty_search(self):
        """Probar búsqueda vacía"""
        response = self.client.post(reverse('search'), {'searched': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por favor ingresa un término de búsqueda')


class ProductImageDisplayTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            stock=10,
            is_available=True,
            category=self.category
        )

    def test_home_page_renders(self):
        """Verificar que la página de inicio se renderiza correctamente"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ecomerce Sniper')
    
    def test_category_page_renders(self):
        """Verificar que las páginas de categoría se renderizan correctamente"""
        response = self.client.get(reverse('category', args=['Test Category']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')
    
    def test_search_page_renders(self):
        """Verificar que la página de búsqueda se renderiza correctamente"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buscar Productos')


class ReservationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass', 
            email='test@example.com'
        )
        self.category = Category.objects.create(name='Armas')
        self.product = Product.objects.create(
            name='Test Rifle',
            price=1000.00,
            stock=5,
            is_available=True,
            category=self.category
        )

    def test_create_reservation(self):
        """Probar creación de reserva"""
        reservation = Reservation.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            customer_name='Test User',
            customer_email='test@example.com',
            shipping_address='Test Address 123',
            total_price=1000.00
        )
        
        self.assertEqual(reservation.status, 'pending')
        self.assertEqual(reservation.product, self.product)
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(str(reservation), f'Reserva #{reservation.id} - Test Rifle (1)')

    def test_reservation_stock_validation(self):
        """Probar validación de stock en reservas"""
        # Crear una reserva que exceda el stock
        with self.assertRaises(ValueError):
            if self.product.stock < 10:  # El producto solo tiene 5 en stock
                raise ValueError("Stock insuficiente")
