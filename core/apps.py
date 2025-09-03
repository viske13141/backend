from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.hashers import make_password


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from .models import AdminUser  # Import inside ready()

        try:
            email = getattr(settings, "DEFAULT_ADMIN_EMAIL", None)
            password = getattr(settings, "DEFAULT_ADMIN_PASSWORD", None)

            if email and password:
                if not AdminUser.objects.filter(email=email).exists():
                    AdminUser.objects.create(
                        email=email,
                        password=make_password(password)  # ✅ Hash password
                    )
        except (OperationalError, ProgrammingError):
            # Happens during migrate when the table isn't ready
            pass
