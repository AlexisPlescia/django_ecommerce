from django.test import TestCase, Client
from .models import Product, Order, Profile, Category, Customer
from django.contrib.auth.models import User
from django.urls import reverse

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
