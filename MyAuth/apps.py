from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError

class MyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myauth'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="iamameer9393_arch"        
                )
                print("✅ Superuser 'admin' created.")
        except (OperationalError, ProgrammingError):
            # Happens during migrations or when DB is not ready
            pass
