#!/bin/bash

# Script de startup para Azure App Service
# Este arquivo será executado durante o deploy

echo "🚀 Iniciando aplicação Django..."

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "🗄️ Executando migrações do banco..."
python manage.py migrate --noinput

# Verificar se o superuser existe, senão criar um padrão
echo "👤 Verificando superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Criando superuser padrão...')
    User.objects.create_superuser('admin', 'admin@exemplo.com', 'admin123')
    print('Superuser criado: admin/admin123')
else:
    print('Superuser já existe')
"

echo "✅ Setup completo! Iniciando servidor..."

# Iniciar o servidor Gunicorn
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info 