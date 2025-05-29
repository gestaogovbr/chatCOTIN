# 🛠️ Guia de Configuração - Ambiente de Desenvolvimento

Este documento fornece instruções **completas e detalhadas** para configurar o ambiente de desenvolvimento local da aplicação Chatbot Django com Databricks/Ollama.

## 📋 **Índice**
- [Pré-requisitos](#pré-requisitos)
- [Configuração do Ollama](#configuração-do-ollama)
- [Configuração da Aplicação](#configuração-da-aplicação)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Executando a Aplicação](#executando-a-aplicação)
- [Verificação do Setup](#verificação-do-setup)
- [Troubleshooting](#troubleshooting)
- [Comandos Úteis](#comandos-úteis)

---

## 🎯 **Pré-requisitos**

### **Software Necessário**

- **Python 3.8+** ([Download](https://python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **VSCode** ou editor de sua preferência
- **Terminal/CMD** com permissões adequadas

### **Verificação dos Pré-requisitos**

```bash
# Verificar versões instaladas
python --version          # Deve ser 3.8+
git --version            # Qualquer versão recente
pip --version            # Geralmente vem com Python
```

**Saída esperada:**
```
Python 3.11.0
git version 2.40.0
pip 23.0.1
```

---

## 🤖 **Configuração do Ollama**

### **Passo 1: Instalação do Ollama**

#### **Windows**
```powershell
# Baixar e instalar do site oficial
# Visite: https://ollama.ai/download
# Execute o instalador .exe baixado
```

#### **macOS**
```bash
# Usando Homebrew (recomendado)
brew install ollama

# Ou baixar do site oficial
# https://ollama.ai/download
```

#### **Linux (Ubuntu/Debian)**
```bash
# Instalação via script oficial
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar instalação
ollama --version
```

### **Passo 2: Iniciar Serviço Ollama**

```bash
# Iniciar Ollama em background
ollama serve

# Em um novo terminal, verificar se está funcionando
curl http://localhost:11434/api/tags
```

**Saída esperada:**
```json
{"models":[]}
```

### **Passo 3: Download do Modelo**

```bash
# Baixar modelo recomendado para desenvolvimento
ollama pull llama2:7b

# Verificar download
ollama list
```

**Saída esperada:**
```
NAME            ID              SIZE    MODIFIED
llama2:7b       78e26419b446    3.8GB   2 minutes ago
```

### **Passo 4: Testar Modelo**

```bash
# Teste rápido do modelo
ollama run llama2:7b "Olá, como você pode me ajudar?"

# Para sair do chat interativo
/bye
```

---

## 💻 **Configuração da Aplicação**

### **Passo 1: Clonar o Repositório**

```bash
# Clonar o projeto
git clone <URL_DO_REPOSITORIO>
cd ia_code_assistance

# Verificar estrutura do projeto
ls -la
```

**Estrutura esperada:**
```
ia_code_assistance/
├── accounts/
├── chatbot/
├── core/
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
└── ...
```

### **Passo 2: Criar Ambiente Virtual**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Verificar ativação (prompt deve mostrar (venv))
which python  # ou where python no Windows
```

**Saída esperada:**
```
# Windows: C:\...\ia_code_assistance\venv\Scripts\python.exe
# macOS/Linux: /path/to/ia_code_assistance/venv/bin/python
```

### **Passo 3: Instalar Dependências**

```bash
# Atualizar pip para última versão
python -m pip install --upgrade pip

# Instalar dependências do projeto
pip install -r requirements.txt

# Verificar instalação
pip list | head -10
```

**Dependências principais esperadas:**
```
Django==5.1.3
python-decouple==3.8
langchain
ollama-python
...
```

---

## 🔧 **Variáveis de Ambiente**

### **Passo 1: Criar Arquivo .env**

```bash
# Copiar template
cp .env.example .env

# Editar arquivo .env
# Windows: notepad .env
# macOS: open -e .env
# Linux: nano .env
```

### **Passo 2: Configurar Variáveis para Desenvolvimento Local**

```env
# .env - Configuração para desenvolvimento local

# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-local-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite para desenvolvimento)
# DATABASE_URL=  # Deixar vazio para usar SQLite

# Ollama Configuration (local)
AI_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b

# Databricks (opcional - para testar integração)
# DATABRICKS_HOST=
# DATABRICKS_TOKEN=
# DATABRICKS_MODEL_ENDPOINT=

# Email (opcional para desenvolvimento)
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### **Passo 3: Validar Configurações**

```bash
# Testar configurações
python -c "
from decouple import config
print('DEBUG:', config('DEBUG'))
print('OLLAMA_BASE_URL:', config('OLLAMA_BASE_URL', default='Not set'))
"
```

---

## 🚀 **Executando a Aplicação**

### **Passo 1: Preparar Banco de Dados**

```bash
# Verificar se há migrações pendentes
python manage.py showmigrations

# Aplicar migrações
python manage.py migrate

# Verificar aplicação
python manage.py showmigrations --plan
```

**Saída esperada:**
```
[X] 0001_initial
[X] 0002_create_superuser
...
```

### **Passo 2: Criar Superusuário (Opcional)**

```bash
# Criar superusuário para acessar admin
python manage.py createsuperuser

# Seguir prompts:
# Username: admin
# Email: admin@localhost.com
# Password: admin123 (ou sua preferência)
```

### **Passo 3: Coletar Arquivos Estáticos**

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Verificar coleta
ls -la staticfiles/  # ou dir staticfiles no Windows
```

### **Passo 4: Verificar Configurações**

```bash
# Executar comando de verificação personalizado
python manage.py check_deployment

# Executar verificações do Django
python manage.py check
```

### **Passo 5: Iniciar Servidor de Desenvolvimento**

```bash
# Iniciar servidor Django
python manage.py runserver

# Ou especificar porta customizada
python manage.py runserver 8080
```

**Saída esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 08, 2024 - 15:30:00
Django version 5.1.3, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

## ✅ **Verificação do Setup**

### **Checklist de Validação**

Execute cada verificação para garantir que tudo está funcionando:

```bash
# 1. ✅ Ollama funcionando
curl -s http://localhost:11434/api/tags | python -m json.tool

# 2. ✅ Aplicação Django rodando
curl -s http://localhost:8000/health/ | python -m json.tool

# 3. ✅ Admin acessível
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/
# Esperado: 200

# 4. ✅ Teste de chat (opcional)
curl -X POST http://localhost:8000/accounts/login/ \
  -d "username=admin&password=admin123" \
  -c cookies.txt

# 5. ✅ Health check completo
python manage.py check_deployment
```

### **URLs para Testar no Browser**

1. **Aplicação Principal**: http://localhost:8000/
2. **Admin Django**: http://localhost:8000/admin/
3. **Health Check**: http://localhost:8000/health/
4. **Status**: http://localhost:8000/status/
5. **Login**: http://localhost:8000/accounts/login/

### **Teste End-to-End**

1. Acesse http://localhost:8000/accounts/login/
2. Faça login com suas credenciais
3. Acesse o chatbot
4. Digite uma pergunta teste: "Olá, como você funciona?"
5. Verifique se recebe resposta do Ollama

---

## 🔧 **Troubleshooting**

### **Problema: Ollama não iniciando**

```bash
# Verificar se porta está em uso
netstat -an | grep 11434

# Matar processo se necessário
pkill ollama

# Reiniciar Ollama
ollama serve
```

### **Problema: Modelo não encontrado**

```bash
# Listar modelos disponíveis
ollama list

# Re-baixar modelo se necessário
ollama pull llama2:7b

# Verificar espaço em disco
df -h  # Linux/macOS
dir   # Windows
```

### **Problema: Erro de dependências Python**

```bash
# Verificar ambiente virtual ativo
which python

# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar conflitos
pip check
```

### **Problema: Erro de migração Django**

```bash
# Reset completo do banco (CUIDADO: apaga dados)
rm db.sqlite3
python manage.py migrate

# Ou verificar migrações específicas
python manage.py showmigrations --verbosity=2
```

### **Problema: Porta 8000 ocupada**

```bash
# Verificar o que está usando a porta
# Windows:
netstat -an | findstr :8000

# Linux/macOS:
lsof -i :8000

# Usar porta alternativa
python manage.py runserver 8080
```

---

## 🎯 **Comandos Úteis**

### **Desenvolvimento Diário**

```bash
# Ativar ambiente e iniciar desenvolvimento
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Iniciar Ollama (se não estiver rodando)
ollama serve &

# Iniciar Django
python manage.py runserver

# Verificar logs em tempo real
tail -f ollama.log  # Se configurado
```

### **Comandos Django Frequentes**

```bash
# Criar nova migração
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Abrir shell Django
python manage.py shell

# Criar superusuário
python manage.py createsuperuser

# Verificar configurações
python manage.py check_deployment
```

### **Comandos Ollama Úteis**

```bash
# Listar modelos instalados
ollama list

# Baixar novo modelo
ollama pull codellama:7b

# Testar modelo via CLI
ollama run llama2:7b "Teste rápido"

# Ver logs do Ollama
ollama logs

# Parar Ollama
ollama stop
```

### **Git Workflow**

```bash
# Verificar status
git status

# Criar nova branch para feature
git checkout -b feature/nova-funcionalidade

# Commit das mudanças
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Push para repositório
git push origin feature/nova-funcionalidade
```

---

## 📝 **Próximos Passos**

### **Para Desenvolvimento**

1. **Configure seu IDE**:
   - Instale extensões Python/Django
   - Configure linting (flake8, black)
   - Configure debugger

2. **Familiarize-se com a estrutura**:
   - Explore `chatbot/` (lógica principal)
   - Entenda `accounts/` (autenticação)
   - Revise `core/` (configurações)

3. **Execute os testes**:
   ```bash
   python manage.py test
   ```

4. **Leia a documentação**:
   - `README.md` - Visão geral
   - `DEPLOY_AZURE.md` - Deploy
   - `OLLAMA_PRODUCTION_GUIDE.md` - Produção

### **Para Contribuição**

1. Siga as convenções de código
2. Escreva testes para novas funcionalidades
3. Atualize documentação quando necessário
4. Use commits semânticos

---

## 📞 **Suporte**

### **Em caso de problemas:**

1. **Verifique os logs**:
   ```bash
   python manage.py runserver --verbosity=2
   ```

2. **Execute diagnóstico**:
   ```bash
   python manage.py check_deployment --fix
   ```

3. **Consulte documentação**:
   - README.md (geral)
   - Issues do repositório

4. **Contato**:
   - Desenvolvedor responsável: [seu-email]
   - Documentação técnica: Issues do GitHub

---

**Criado em**: $(date)  
**Versão**: 1.0  
**Ambiente**: Desenvolvimento Local 