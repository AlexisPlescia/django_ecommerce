Django Ecommerce
Este proyecto es una plataforma de comercio electrónico desarrollada con Django. Permite a los usuarios navegar, registrarse, iniciar sesión, agregar productos al carrito, realizar compras y gestionar pedidos. Incluye funcionalidades de autenticación, gestión de pagos, panel de administración y pruebas automatizadas (unitarias y end-to-end).

Características principales:

Catálogo de productos y categorías.
Carrito de compras y resumen.
Registro e inicio de sesión de usuarios.
Proceso de pago y gestión de pedidos.
Panel de administración para gestión de productos y ventas.
Pruebas automatizadas (unitarias y E2E con pytest).
Estructura modular y escalable.
Tecnologías utilizadas:

Python 3
Django
HTML, CSS, JavaScript
Pytest (para testing)
SQLite (por defecto, fácilmente adaptable a otros motores)
Estructura principal:

store: Lógica y vistas de productos, usuarios y categorías.
cart: Funcionalidad de carrito de compras.
payment: Gestión de pagos y pedidos.
e2e_test: Pruebas end-to-end automatizadas.
static y media: Archivos estáticos e imágenes.
