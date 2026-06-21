import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Mfumo wa dharura wa kulazimisha Migration, Kufungua Lockout, na kuunda Admin mpya
try:
    import django
    django.setup()
    
    # 1. Pigia migration mtandaoni
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
    
    # 2. Safisha lockouts zote zilizowahi kufanyika ili uweze ku-login tena
    from axes.utils import reset
    reset()
    print("Axes lockouts zote zimesafishwa kwa usalama!")
    
    # 3. Tengeneza Superuser (Admin) mpya mtandaoni au sasisha nenosiri lake
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@iaa.ac.tz', 'IAAcyber2026!')
        print("Admin wa dharura ametengenezwa!")
    else:
        u = User.objects.get(username='admin')
        u.set_password('IAAcyber2026!')
        u.save()
        print("Password ya admin imesasishwa!")
except Exception as e:
    print(f"Kosa wakati wa kuwasha WSGI script: {e}")

application = get_wsgi_application()