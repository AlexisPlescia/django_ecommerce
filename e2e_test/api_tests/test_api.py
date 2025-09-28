"""
Tests de API para el backend del ecommerce
Incluye tests para endpoints REST si existen
"""
import pytest
import requests
import json

class TestAPI:
    """Suite de tests para API del ecommerce"""
    
    BASE_URL = "http://127.0.0.1:8001"
    
    @pytest.mark.api
    def test_home_endpoint_responds(self):
        """Verificar que el endpoint principal responde"""
        response = requests.get(f"{self.BASE_URL}/")
        assert response.status_code == 200, "El endpoint principal no responde correctamente"
        assert "text/html" in response.headers.get("content-type", ""), "No devuelve HTML"
    
    @pytest.mark.api
    def test_login_endpoint_responds(self):
        """Verificar que el endpoint de login responde"""
        response = requests.get(f"{self.BASE_URL}/login")
        assert response.status_code == 200, "El endpoint de login no responde"
    
    @pytest.mark.api
    def test_register_endpoint_responds(self):
        """Verificar que el endpoint de registro responde"""
        response = requests.get(f"{self.BASE_URL}/register")
        assert response.status_code == 200, "El endpoint de registro no responde"
    
    @pytest.mark.api
    def test_cart_endpoint_responds(self):
        """Verificar que el endpoint del carrito responde"""
        response = requests.get(f"{self.BASE_URL}/cart")
        assert response.status_code == 200, "El endpoint del carrito no responde"
    
    @pytest.mark.api
    def test_static_files_serve(self):
        """Verificar que los archivos estáticos se sirven correctamente"""
        # Test CSS
        response = requests.get(f"{self.BASE_URL}/static/css/styles.css")
        assert response.status_code == 200, "CSS no se sirve correctamente"
        assert "text/css" in response.headers.get("content-type", ""), "CSS no tiene content-type correcto"
        
        # Test JS
        response = requests.get(f"{self.BASE_URL}/static/js/scripts.js")
        assert response.status_code == 200, "JS no se sirve correctamente"
    
    @pytest.mark.api
    def test_invalid_urls_return_404(self):
        """Verificar que URLs inválidas devuelven 404"""
        invalid_urls = [
            "/pagina-inexistente",
            "/producto/999999",
            "/category/inexistente",
            "/usuario/inexistente"
        ]
        
        for url in invalid_urls:
            response = requests.get(f"{self.BASE_URL}{url}")
            assert response.status_code == 404, f"URL {url} no devuelve 404"
    
    @pytest.mark.api
    def test_post_login_functionality(self):
        """Probar funcionalidad POST de login"""
        login_data = {
            "username": "usuario_test",
            "password": "contraseña_test"
        }
        
        # Primero obtener la página de login para el token CSRF
        session = requests.Session()
        login_page = session.get(f"{self.BASE_URL}/login")
        
        # Intentar login (debería fallar con credenciales incorrectas)
        response = session.post(f"{self.BASE_URL}/login", data=login_data)
        
        # Verificar que no se redirigió exitosamente
        assert response.status_code in [200, 302], "Respuesta inesperada del login"
    
    @pytest.mark.api
    def test_csrf_protection(self):
        """Verificar que hay protección CSRF"""
        # Intentar POST sin token CSRF
        response = requests.post(f"{self.BASE_URL}/login", data={
            "username": "test",
            "password": "test"
        })
        
        # Django debería rechazar requests sin CSRF token
        assert response.status_code == 403, "No hay protección CSRF"
    
    @pytest.mark.api
    def test_search_functionality(self):
        """Probar funcionalidad de búsqueda"""
        search_data = {
            "searched": "producto"
        }
        
        session = requests.Session()
        # Obtener página principal primero
        session.get(f"{self.BASE_URL}/")
        
        # Intentar búsqueda
        response = session.post(f"{self.BASE_URL}/search", data=search_data)
        
        assert response.status_code in [200, 302], "Búsqueda no funciona correctamente"
    
    @pytest.mark.api
    def test_response_times(self):
        """Probar tiempos de respuesta de endpoints principales"""
        endpoints = [
            "/",
            "/login",
            "/register",
            "/cart"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            assert response.elapsed.total_seconds() < 5, f"Endpoint {endpoint} es muy lento"
    
    @pytest.mark.api
    def test_security_headers(self):
        """Verificar headers de seguridad básicos"""
        response = requests.get(f"{self.BASE_URL}/")
        
        headers = response.headers
        
        # Verificar algunos headers de seguridad (pueden no estar todos configurados)
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block"
        }
        
        # Al menos algunos headers de seguridad deberían estar presentes
        security_headers_present = sum(1 for header in security_headers.keys() if header in headers)
        assert security_headers_present > 0, "No hay headers de seguridad configurados"
    
    @pytest.mark.api
    def test_content_encoding(self):
        """Verificar que el contenido se envía correctamente"""
        response = requests.get(f"{self.BASE_URL}/")
        
        # Verificar que el contenido tiene codificación UTF-8
        assert "charset=utf-8" in response.headers.get("content-type", "").lower(), "No hay codificación UTF-8"
    
    @pytest.mark.api
    def test_admin_endpoints_protection(self):
        """Verificar que los endpoints de admin están protegidos"""
        admin_endpoints = [
            "/admin/",
            "/shipped_dash",
            "/not_shipped_dash"
        ]
        
        for endpoint in admin_endpoints:
            response = requests.get(f"{self.BASE_URL}{endpoint}")
            # Debería redirigir a login o devolver 403/404
            assert response.status_code in [302, 403, 404], f"Endpoint admin {endpoint} no está protegido"
    
    @pytest.mark.api
    def test_http_methods_allowed(self):
        """Verificar métodos HTTP permitidos"""
        # GET debería estar permitido en páginas principales
        response = requests.get(f"{self.BASE_URL}/")
        assert response.status_code == 200, "GET no permitido en home"
        
        # POST debería estar permitido en login
        response = requests.post(f"{self.BASE_URL}/login", data={})
        assert response.status_code != 405, "POST no permitido en login"
        
        # PUT/DELETE no deberían estar permitidos en páginas normales
        response = requests.put(f"{self.BASE_URL}/")
        assert response.status_code == 405, "PUT debería estar prohibido"
        
        response = requests.delete(f"{self.BASE_URL}/")
        assert response.status_code == 405, "DELETE debería estar prohibido"
    
    @pytest.mark.api
    def test_session_handling(self):
        """Probar manejo de sesiones"""
        session = requests.Session()
        
        # Primera request
        response1 = session.get(f"{self.BASE_URL}/")
        assert response1.status_code == 200
        
        # Segunda request con la misma sesión
        response2 = session.get(f"{self.BASE_URL}/cart")
        assert response2.status_code == 200
        
        # Verificar que se mantiene la sesión
        cookies1 = response1.cookies
        cookies2 = response2.cookies
        
        # Debería haber cookies de sesión
        assert len(cookies1) > 0 or len(cookies2) > 0, "No hay manejo de sesiones"
    
    @pytest.mark.api
    def test_database_connectivity(self):
        """Verificar conectividad con base de datos (indirectamente)"""
        # Si la aplicación carga, la base de datos debería estar conectada
        response = requests.get(f"{self.BASE_URL}/")
        assert response.status_code == 200, "Posible problema de conectividad con BD"
        
        # Verificar que se pueden mostrar productos (requiere BD)
        assert "producto" in response.text.lower() or "product" in response.text.lower(), "No se cargan datos de BD"
    
    @pytest.mark.api
    def test_error_handling(self):
        """Probar manejo de errores"""
        # URL que debería generar error 404
        response = requests.get(f"{self.BASE_URL}/pagina-inexistente")
        assert response.status_code == 404, "No se maneja error 404"
        
        # Verificar que la página de error no expone información sensible
        assert "traceback" not in response.text.lower(), "La página de error expone información sensible"
        assert "exception" not in response.text.lower(), "La página de error expone información sensible"
    
    @pytest.mark.api
    def test_redirect_handling(self):
        """Probar manejo de redirects"""
        # Intentar acceder a página que requiere login
        response = requests.get(f"{self.BASE_URL}/update_user", allow_redirects=False)
        
        # Debería redirigir
        assert response.status_code in [302, 301], "No se redirige correctamente"
        
        # Verificar que la redirección es apropiada
        location = response.headers.get("location", "")
        assert "login" in location.lower() or location == "/", "Redirección no es apropiada"
