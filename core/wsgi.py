import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 1. Kupiga Migrate kiotomatiki
try:
    from django.core.management import execute_from_command_line
    print("Inalazimisha migrations kufanya kazi...")
    execute_from_command_line([sys.argv[0], 'migrate', '--noinput'])
except Exception as e:
    print(f"Migration imefeli: {e}")

# 2. Kutengeneza Superuser wa dharura mtandaoni
try:
    import django
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Angalia kama admin tayari yupo, kama hayapo mtengeneze
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@iaa.ac.tz', 'IAAcyber2026!')
        print("Superuser 'admin' ametengenezwa kikamilifu!")
    else:
        # Kama yupo, tunamgeuzia password kuwa hii mpya kabisa
        u = User.objects.get(username='admin')
        u.set_password('IAAcyber2026!')
        u.save()
        print("Password ya 'admin' imesasishwa!")
except Exception as e:
    print(f"Kosa la kutengeneza superuser: {e}")

application = get_wsgi_application()