"""
Middleware para contar visitas al sitio web
"""
import re
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.db.models import F
from store.models import VisitCounter, VisitSummary
from django.contrib.auth.models import User

def get_client_ip(request):
    """Obtener la IP real del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def detect_mobile(user_agent):
    """Detectar si es un dispositivo móvil"""
    mobile_patterns = [
        r'Mobile', r'Android', r'iPhone', r'iPad', r'Windows Phone',
        r'BlackBerry', r'Opera Mini', r'IEMobile'
    ]
    
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True
    return False

def parse_user_agent(user_agent):
    """Parsear información del user agent"""
    browser = "Unknown"
    os = "Unknown"
    
    # Detectar navegador
    if 'Chrome' in user_agent:
        browser = "Chrome"
    elif 'Firefox' in user_agent:
        browser = "Firefox"
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        browser = "Safari"
    elif 'Edge' in user_agent:
        browser = "Edge"
    elif 'Opera' in user_agent:
        browser = "Opera"
    
    # Detectar sistema operativo
    if 'Windows' in user_agent:
        os = "Windows"
    elif 'Mac OS X' in user_agent or 'macOS' in user_agent:
        os = "macOS"
    elif 'Linux' in user_agent:
        os = "Linux"
    elif 'Android' in user_agent:
        os = "Android"
    elif 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        os = "iOS"
    
    return browser, os

class VisitCounterMiddleware(MiddlewareMixin):
    """Middleware para contar visitas automáticamente"""
    
    def process_request(self, request):
        # Solo contar visitas GET (no AJAX, POST, etc.)
        if request.method != 'GET':
            return None
        
        # Ignorar ciertos paths
        ignore_paths = [
            '/admin/', '/static/', '/media/', '/favicon.ico',
            '/robots.txt', '/sitemap.xml'
        ]
        
        for ignore_path in ignore_paths:
            if request.path.startswith(ignore_path):
                return None
        
        # Obtener información de la visita
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        page_url = request.build_absolute_uri()
        referrer = request.META.get('HTTP_REFERER', '')
        
        # Información del dispositivo
        is_mobile = detect_mobile(user_agent)
        browser, operating_system = parse_user_agent(user_agent)
        
        # Usuario (si está logueado)
        user = request.user if request.user.is_authenticated else None
        
        try:
            # Crear registro de visita con timestamp timezone-aware
            visit = VisitCounter.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                user=user,
                page_url=page_url,
                referrer=referrer or None,
                is_mobile=is_mobile,
                browser=browser,
                operating_system=operating_system,
                timestamp=timezone.now()  # Usar timezone.now() explícitamente
            )
            
            # Actualizar resumen diario
            today = timezone.now().date()
            summary, created = VisitSummary.objects.get_or_create(
                date=today,
                defaults={
                    'total_visits': 0,
                    'unique_visitors': 0,
                    'logged_users_visits': 0,
                    'anonymous_visits': 0,
                    'mobile_visits': 0,
                    'desktop_visits': 0,
                }
            )
            
            # Incrementar contadores
            summary.total_visits = F('total_visits') + 1
            
            if user:
                summary.logged_users_visits = F('logged_users_visits') + 1
            else:
                summary.anonymous_visits = F('anonymous_visits') + 1
            
            if is_mobile:
                summary.mobile_visits = F('mobile_visits') + 1
            else:
                summary.desktop_visits = F('desktop_visits') + 1
            
            summary.save()
            
            # Calcular visitantes únicos (por IP) del día
            unique_ips_today = VisitCounter.objects.filter(
                timestamp__date=today
            ).values('ip_address').distinct().count()
            
            summary.unique_visitors = unique_ips_today
            summary.save(update_fields=['unique_visitors'])
            
        except Exception as e:
            # En caso de error, no interrumpir la petición
            print(f"Error logging visit: {e}")
        
        return None
