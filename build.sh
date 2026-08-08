#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Namunaviy mahsulotlarni yuklash (xavfsiz — mavjud bo'lsa qayta yozadi, xato bermaydi)
python manage.py loaddata sample_products || true

# Superuser yaratish (agar DJANGO_SUPERUSER_* muhit o'zgaruvchilari berilgan bo'lsa)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

