# 🗄️ GUIA COMPLETO: MIGRAÇÃO SQLite → PostgreSQL
## ChatCOTIN - Sistema de IA para Dados Abertos

---

## 📋 **ÍNDICE**
1. [Pré-requisitos](#pré-requisitos)
2. [Backup dos Dados](#backup-dos-dados)
3. [Instalação do PostgreSQL](#instalação-do-postgresql)
4. [Configuração do Banco](#configuração-do-banco)
5. [Configuração do Django](#configuração-do-django)
6. [Execução das Migrações](#execução-das-migrações)
7. [Verificação e Testes](#verificação-e-testes)
8. [Solução de Problemas](#solução-de-problemas)

---

## 🎯 **PRÉ-REQUISITOS**

### **Dependências Python**
```bash
# Verificar se estão no requirements.txt:
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### **Ambiente Virtual Ativo**
```bash
# Windows
./venv312/Scripts/activate

# Linux/Mac
source venv312/bin/activate
```

---

## 💾 **ETAPA 1: BACKUP DOS DADOS**

### **1.1 Criar Backup Completo**
```bash
# Backup dos dados SQLite existentes
python manage.py dumpdata --indent=2 --output=backup_dados_chatcotin.json
```

### **1.2 Verificar Backup**
```bash
# Verificar se o arquivo foi criado
ls -la backup_dados_chatcotin.json

# Deverá mostrar o arquivo com tamanho considerável
```

---

## 🐘 **ETAPA 2: INSTALAÇÃO DO POSTGRESQL**

### **2.1 Instalação no Windows**

#### **Opção A: Via winget (Recomendado)**
```bash
winget install PostgreSQL.PostgreSQL
```

#### **Opção B: Download Manual**
1. Acesse: https://www.postgresql.org/download/windows/
2. Baixe o instalador oficial
3. Execute e siga o assistente

### **2.2 Configurações da Instalação**
- **Senha do superusuário (postgres)**: Anote bem!
- **Porta**: 5432 (padrão)
- **Locale**: Portuguese, Brazil

### **2.3 Adicionar ao PATH**

#### **Temporário (por sessão)**
```powershell
# PowerShell
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"
```

#### **Permanente**
```powershell
# PowerShell como Administrador
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\PostgreSQL\17\bin", [EnvironmentVariableTarget]::Machine)
```

### **2.4 Testar Instalação**
```bash
psql --version
# Deve retornar: psql (PostgreSQL) 17.x
```

---

## 🔧 **ETAPA 3: CONFIGURAÇÃO DO BANCO**

### **3.1 Conectar como Superusuário**
```bash
psql -U postgres
# Inserir senha do postgres
```

### **3.2 Comandos SQL no PostgreSQL**
```sql
-- 1. Criar usuário específico
CREATE USER chatcotin_user WITH PASSWORD 'ChatCOTIN2025';

-- 2. Criar banco de dados
CREATE DATABASE chatcotin_db OWNER chatcotin_user;

-- 3. Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE chatcotin_db TO chatcotin_user;

-- 4. Permissão para criar bancos (testes)
ALTER USER chatcotin_user CREATEDB;

-- 5. Verificar criação
\l

-- 6. Sair
\q
```

### **3.3 Testar Conexão**
```bash
# Definir senha como variável de ambiente
export PGPASSWORD="ChatCOTIN2025"  # Linux/Mac
$env:PGPASSWORD="ChatCOTIN2025"    # Windows PowerShell

# Testar conexão
psql -U chatcotin_user -d chatcotin_db -c "SELECT version();"
```

---

## ⚙️ **ETAPA 4: CONFIGURAÇÃO DO DJANGO**

### **4.1 Atualizar settings.py**

Adicionar configuração flexível no arquivo `core/settings.py`:

```python
# Database - Configuração flexível SQLite ou PostgreSQL
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    # Configuração via DATABASE_URL (PostgreSQL)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Configuração individual ou fallback para SQLite
    DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')
    
    if DB_ENGINE == 'django.db.backends.postgresql':
        # PostgreSQL configurado individualmente
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': config('DB_NAME', default='chatcotin_db'),
                'USER': config('DB_USER', default='chatcotin_user'),
                'PASSWORD': config('DB_PASSWORD', default=''),
                'HOST': config('DB_HOST', default='localhost'),
                'PORT': config('DB_PORT', default='5432'),
                'OPTIONS': {
                    'client_encoding': 'UTF8',
                },
            }
        }
    else:
        # SQLite (desenvolvimento/fallback)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
```

### **4.2 Configurar Arquivo .env**

Adicionar no arquivo `.env`:

```bash
# ==============================================
# CONFIGURAÇÕES DO BANCO DE DADOS POSTGRESQL
# ==============================================

# Opção 1: URL completa (mais simples)
DATABASE_URL=postgresql://chatcotin_user:ChatCOTIN2025@localhost:5432/chatcotin_db

# Opção 2: Configuração individual (mais flexível)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chatcotin_db
DB_USER=chatcotin_user
DB_PASSWORD=ChatCOTIN2025
DB_HOST=localhost
DB_PORT=5432
```

**⚠️ IMPORTANTE**: Não use caracteres especiais (`@`, `!`, etc.) na senha para evitar problemas de encoding.

### **4.3 Instalar Dependências**
```bash
pip install psycopg2-binary==2.9.9 dj-database-url==2.1.0
```

---

## 🚀 **ETAPA 5: EXECUÇÃO DAS MIGRAÇÕES**

### **5.1 Testar Conexão Django**
```bash
python manage.py check --database default
# Deve retornar: System check identified no issues
```

### **5.2 Executar Migrações**
```bash
python manage.py migrate
```

**Saída esperada:**
```
Running migrations:
  Applying admin.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  ...
  Applying chatbot.0001_initial... OK
  Applying chatbot.0002_chat_user... OK
  ...
```

### **5.3 Criar Superusuário**
```bash
python manage.py createsuperuser
```

---

## ✅ **ETAPA 6: VERIFICAÇÃO E TESTES**

### **6.1 Verificar Dados**
```bash
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.contrib.auth.models import User
from chatbot.models import *
print('Usuários:', User.objects.count())
print('Chats:', Chat.objects.count())
print('Conversas:', Conversation.objects.count())
"
```

### **6.2 Testar Servidor**
```bash
python manage.py runserver 8000
```

Acessar: http://localhost:8000

### **6.3 Verificar no PostgreSQL**
```bash
psql -U chatcotin_user -d chatcotin_db
```

```sql
-- Listar tabelas
\dt

-- Verificar usuários
SELECT count(*) FROM auth_user;

-- Verificar chats
SELECT count(*) FROM chatbot_chat;

-- Sair
\q
```

---

## 🔄 **ETAPA 7: MIGRAÇÃO DE DADOS (Opcional)**

### **7.1 Importar Backup**
```bash
# Se não há problemas de encoding:
python manage.py loaddata backup_dados_chatcotin.json
```

### **7.2 Em Caso de Problemas de Encoding**

Criar configuração temporária SQLite (`core/settings_sqlite_temp.py`):
```python
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Gerar backup limpo:
```bash
python manage.py dumpdata --indent=2 --output=backup_limpo.json --settings=core.settings_sqlite_temp
```

---

## 🛠️ **SOLUÇÃO DE PROBLEMAS**

### **Problema 1: Erro de Encoding UTF-8**
```bash
# Configurar variáveis de ambiente
export PYTHONIOENCODING="utf-8"    # Linux/Mac
export PYTHONUTF8="1"              # Linux/Mac

$env:PYTHONIOENCODING="utf-8"      # Windows
$env:PYTHONUTF8="1"                # Windows
```

### **Problema 2: PostgreSQL não reconhecido**
```bash
# Adicionar ao PATH
$env:PATH += ";C:\Program Files\PostgreSQL\17\bin"
```

### **Problema 3: Senha com caracteres especiais**
- Use senhas simples sem `@`, `!`, `%`, etc.
- Prefira letras, números e hífen

### **Problema 4: Conexão recusada**
```bash
# Verificar se PostgreSQL está rodando
Get-Service -Name "*postgres*"

# Ou verificar processos
Get-Process postgres
```

### **Problema 5: Permissão negada**
```sql
-- Conectar como postgres e dar permissões
psql -U postgres
GRANT ALL PRIVILEGES ON DATABASE chatcotin_db TO chatcotin_user;
ALTER USER chatcotin_user CREATEDB;
```

---

## 📊 **VERIFICAÇÃO FINAL**

### **Checklist de Sucesso:**
- [ ] PostgreSQL 17+ instalado
- [ ] Banco `chatcotin_db` criado
- [ ] Usuário `chatcotin_user` configurado
- [ ] Django conecta ao PostgreSQL
- [ ] Migrações executadas com sucesso
- [ ] Superusuário criado
- [ ] Sistema roda em http://localhost:8000
- [ ] Interface funciona normalmente

---

## 🎉 **PARABÉNS!**

**Migração concluída com sucesso!** 

O ChatCOTIN agora roda 100% em PostgreSQL, oferecendo:
- ✅ **Melhor performance**
- ✅ **Maior robustez**
- ✅ **Preparado para produção**
- ✅ **Suporte completo a UTF-8**
- ✅ **Recursos avançados de banco**

---

## 📚 **RECURSOS ADICIONAIS**

### **Comandos Úteis PostgreSQL:**
```sql
-- Listar bancos
\l

-- Conectar a outro banco
\c nome_do_banco

-- Listar tabelas
\dt

-- Descrever tabela
\d nome_da_tabela

-- Mostrar usuários
\du

-- Sair
\q
```

### **Backup e Restore PostgreSQL:**
```bash
# Backup
pg_dump -U chatcotin_user chatcotin_db > backup.sql

# Restore
psql -U chatcotin_user chatcotin_db < backup.sql
```

---
**Documentação criada em:** Janeiro 2025  
**Sistema:** ChatCOTIN v2.0  
**Autor:** Assistente IA Claude 4 