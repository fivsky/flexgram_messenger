#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from django.contrib.auth.models import User; User.objects.create_superuser('flexadmin', '', 'Flexgram2026!') if not User.objects.filter(username='flexadmin').exists() else print('admin exists')"
