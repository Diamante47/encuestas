import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas.settings')  # Reemplaza 'encuestas.settings' por tu archivo de configuración
django.setup()

from django.contrib.auth.models import User

# Detalles del superusuario
username = 'Josue'
email = 'superusuario@example.com'
password = 'Diamante3000'

# Verifica si el superusuario ya existe
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superusuario "{username}" creado exitosamente.')
else:
    print(f'El superusuario "{username}" ya existe.')