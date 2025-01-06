#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encuestas.settings')  # Reemplaza 'encuestas.settings' con tu archivo de configuración
django.setup()

from django.contrib.auth.models import User

username = 'nuevo_superusuario'
email = 'superusuario@example.com'
password = 'contraseña_segura'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superusuario "{username}" creado exitosamente.')
else:
    print(f'El superusuario "{username}" ya existe.')
