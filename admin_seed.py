from django.contrib.auth import get_user_model

User = get_user_model()

email = "admin@gmail.com"
username = "admin"
password = "admin1234"

if not User.objects.filter(email=email).exists():
    print("Creating admin user...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("Admin user already exists.")
