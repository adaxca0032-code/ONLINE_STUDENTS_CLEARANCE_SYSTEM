import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Kazi ya kulazimisha migration mtandaoni kiotomatiki
try:
    from django.core.management import execute_from_command_line
    print("Inalazimisha migrations kufanya kazi mtandaoni...")
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
except Exception as e:
    print(f"Migration imefeli lakini tunawasha mtambo: {e}")

application = get_wsgi_application()