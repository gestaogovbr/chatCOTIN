# Configuração temporária para usar SQLite
from .settings import *

# Forçar SQLite independente das variáveis de ambiente
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 