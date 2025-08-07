"""
Providers Django app configuration.
"""

from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    """Configuration for providers app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'providers'
    verbose_name = 'Healthcare Providers' 