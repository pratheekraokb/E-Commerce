# In E_Commerce_app/apps.py
from django.apps import AppConfig

class ECommerceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'E_Commerce_app'
    verbose_name = 'E Commerce App'

    def ready(self):
        import E_Commerce_app.signals  # Import your signals module
