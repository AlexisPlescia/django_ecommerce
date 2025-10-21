from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class VisitCounter(models.Model):
    """Modelo para contar visitas al sitio"""
    
    # Información básica de la visita
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Usuario (si está logueado)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Información de la página visitada
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    
    # Información del dispositivo/navegador
    is_mobile = models.BooleanField(default=False)
    browser = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    
    # Información geográfica (opcional, para futuro)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-timestamp']
    
    def __str__(self):
        user_info = f"Usuario: {self.user.username}" if self.user else f"IP: {self.ip_address}"
        return f"{user_info} - {self.page_url} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

class VisitSummary(models.Model):
    """Resumen diario de visitas para mejor rendimiento"""
    
    date = models.DateField(unique=True)
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    logged_users_visits = models.PositiveIntegerField(default=0)
    anonymous_visits = models.PositiveIntegerField(default=0)
    mobile_visits = models.PositiveIntegerField(default=0)
    desktop_visits = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Resumen de Visitas'
        verbose_name_plural = 'Resúmenes de Visitas'
        ordering = ['-date']
    
    def __str__(self):
        return f"Visitas del {self.date.strftime('%d/%m/%Y')}: {self.total_visits} total"
