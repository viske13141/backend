from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        from .models import AdminUser  # Import here to avoid AppRegistryNotReady errors
        try:
            email = settings.DEFAULT_ADMIN_EMAIL
            password = settings.DEFAULT_ADMIN_PASSWORD
            if not AdminUser.objects.filter(email=email).exists():
                AdminUser.objects.create(email=email, password=password)
        except (OperationalError, ProgrammingError):
            # Happens during `migrate` when table isn't created yet
            pass