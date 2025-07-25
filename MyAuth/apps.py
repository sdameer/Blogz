# myauth/apps.py

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError, ProgrammingError
import logging

class MyauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MyAuth'

    def ready(self):
        try:
            User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin1234"
                )
                logging.info("✅ Superuser created: admin / admin1234")
        except (OperationalError, ProgrammingError):
            pass  # DB might not be ready during migration
