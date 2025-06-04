# 🛠️ Guia de Configuração - Ambiente de Desenvolvimento (Atualizado)

Este documento fornece instruções **completas e atualizadas** para configurar o ambiente de desenvolvimento local da aplicação ChatCOTIN Django com **Databricks e Groq Cloud**.

## 📋 **Índice**
- [Pré-requisitos](#pré-requisitos)
- [Configuração das APIs de IA](#configuração-das-apis-de-ia)
- [Configuração da Aplicação](#configuração-da-aplicação)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Executando a Aplicação](#executando-a-aplicação)
- [Verificação do Setup](#verificação-do-setup)
- [Troubleshooting](#troubleshooting)
- [Comandos Úteis](#comandos-úteis)

---

## 🎯 **Pré-requisitos**

### **Software Necessário**

- **Python 3.12+** ([Download](https://python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **VSCode** ou editor de sua preferência
- **Terminal/CMD** com permissões adequadas

### **Contas de API Necessárias**

- **Conta Databricks** (para modelo principal)
- **Conta Groq Cloud** (para modelo alternativo)

### **Verificação dos Pré-requisitos**

```bash
# Verificar versões instaladas
python --version          # Deve ser 3.12+
git --version            # Qualquer versão recente
pip --version            # Geralmente vem com Python
```

**Saída esperada:**
```
Python 3.12.0
git version 2.40.0
pip 23.0.1
```

---

## 🤖 **Configuração das APIs de IA**

### **Passo 1: Configurar Databricks**

1. **Acessar Databricks Console**
   - Acesse [databricks.com](https://databricks.com)
   - Faça login em sua conta

2. **Obter Token de Acesso**
   ```bash
   # Vá para: User Settings > Access Tokens
   # Clique em "Generate New Token"
   # Salve o token gerado (será usado no .env)
   ```

3. **Configurar Endpoint do Modelo**
   ```bash
   # Vá para: Serving > Model Serving
   # Localize seu endpoint de modelo
   # Copie a URL do endpoint
   ```

### **Passo 2: Configurar Groq Cloud**

1. **Criar Conta Groq**
   - Acesse [console.groq.com](https://console.groq.com)
   - Registre-se ou faça login

2. **Obter API Key**
   ```bash
   # Vá para: API Keys
   # Clique em "Create API Key"
   # Salve a chave (formato: gsk_...)
   ```

3. **Verificar Modelo Disponível**
   - Modelo utilizado: `llama-3.3-70b-versatile`
   - Verifique disponibilidade na documentação Groq

---

## 💻 **Configuração da Aplicação**

### **Passo 1: Clonar o Repositório**

```bash
# Clonar o projeto
git clone <URL_DO_REPOSITORIO>
cd chatCOTIN

# Verificar estrutura do projeto
ls -la
```

**Estrutura esperada:**
```
chatCOTIN/
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
# Criar ambiente virtual Python 3.12
python -m venv venv312

# Ativar ambiente virtual
# Windows:
venv312\Scripts\activate

# macOS/Linux:
source venv312/bin/activate

# Verificar ativação (prompt deve mostrar (venv312))
which python  # ou where python no Windows
```

**Saída esperada:**
```
# Windows: C:\...\chatCOTIN\venv312\Scripts\python.exe
# macOS/Linux: /path/to/chatCOTIN/venv312/bin/python
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
Django==5.2.1
python-decouple==3.8
langchain
groq
databricks-langchain==0.5.1
chromadb==1.0.11
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

### **Passo 2: Configurar Variáveis**

```env
# === CONFIGURAÇÕES GERAIS ===
SECRET_KEY=sua-chave-secreta-django-muito-longa-e-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# === DATABRICKS CONFIGURATION ===
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi-seu-token-databricks-aqui
DATABRICKS_MODEL_ENDPOINT=seu-endpoint-modelo-aqui

# === GROQ CLOUD CONFIGURATION ===
GROQ_API_KEY=gsk_sua_chave_groq_aqui

# === DATABASE (SQLite para desenvolvimento) ===
DATABASE_URL=sqlite:///db.sqlite3

# === CONFIGURAÇÕES OPCIONAIS ===
LLM_PROVIDER=databricks  # ou 'groq'
```

### **Passo 3: Verificar Configurações**

```python
# Criar arquivo test_config.py
from decouple import config

print('=== VERIFICAÇÃO DE CONFIGURAÇÕES ===')
print('SECRET_KEY:', 'OK' if config('SECRET_KEY', default='') else 'FALTANDO')
print('DATABRICKS_HOST:', config('DATABRICKS_HOST', default='Not set'))
print('DATABRICKS_TOKEN:', 'OK' if config('DATABRICKS_TOKEN', default='') else 'FALTANDO')
print('GROQ_API_KEY:', 'OK' if config('GROQ_API_KEY', default='') else 'FALTANDO')
```

```bash
# Executar verificação
python test_config.py
```

---

## 🚀 **Executando a Aplicação**

### **Passo 1: Configurar Base de Dados**

```bash
# Aplicar migrações do banco
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser
```

### **Passo 2: Iniciar Servidor de Desenvolvimento**

```bash
# Iniciar servidor Django
python manage.py runserver

# Aplicação estará disponível em:
# http://127.0.0.1:8000/
```

### **Passo 3: Acessar Interface**

1. **Login/Registro**: `http://127.0.0.1:8000/accounts/login/`
2. **ChatCOTIN**: `http://127.0.0.1:8000/chatbot/`
3. **Admin**: `http://127.0.0.1:8000/admin/` (se criou superusuário)

---

## ✅ **Verificação do Setup**

### **Checklist de Funcionamento**

```bash
# 1. ✅ Python 3.12 ativo
python --version

# 2. ✅ Dependências instaladas
pip check

# 3. ✅ Django funcionando
python manage.py check

# 4. ✅ Variáveis configuradas
python test_config.py

# 5. ✅ Servidor rodando
curl http://127.0.0.1:8000/
```

### **Teste dos Modelos de IA**

1. **Acesse o ChatCOTIN**
2. **Teste modelo Databricks** (padrão)
3. **Teste modelo Groq** (configurações)
4. **Verifique se recebe respostas dos dois modelos**

---

## 🛠️ **Troubleshooting**

### **Problema: Erro de dependências**

```bash
# Limpar cache pip
pip cache purge

# Reinstalar dependências
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### **Problema: Erro de API Keys**

```bash
# Verificar se as chaves estão corretas
python -c "from decouple import config; print(config('GROQ_API_KEY'))"

# Testar conexão Databricks
python -c "from databricks_langchain import ChatDatabricks; print('Databricks OK')"

# Testar conexão Groq
python -c "from groq import Groq; client = Groq(); print('Groq OK')"
```

### **Problema: Porta em uso**

```bash
# Verificar processo usando porta 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Matar processo se necessário
# Windows:
taskkill /PID <PID> /F

# macOS/Linux:
kill -9 <PID>
```

---

## 🔧 **Comandos Úteis**

### **Comandos Django**

```bash
# Verificar status do projeto
python manage.py check

# Criar nova migração
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test
```

### **Comandos de Desenvolvimento**

```bash
# Ativar ambiente virtual rapidamente
# Windows:
venv312\Scripts\activate

# macOS/Linux:
source venv312/bin/activate

# Verificar logs em tempo real
python manage.py runserver --verbosity=2

# Executar em modo debug avançado
python manage.py runserver --settings=core.settings.debug
```

---

## 📚 **Próximos Passos**

Após concluir este setup, consulte:

- 📖 **[README.md](README.md)** - Visão geral do projeto
- 🔄 **[Atualização da Base](COMO_ATUALIZAR_BASE_CONHECIMENTO.md)** - Como incluir novos documentos
- ☁️ **[Deploy Azure](DEPLOY_AZURE.md)** - Guia para produção
- 🚀 **[Configuração Groq](CONFIGURACAO_GROQ.md)** - Detalhes do modelo Groq

---

## 📞 **Suporte**

Para dúvidas ou problemas:
- **Equipe COTIN**: Coordenação de Transparência e Informações Gerenciais
- **Coordenador**: Magnum Costa de Oliveira
- **Desenvolvedores**: Guilherme Fonseca, Stefano Terci, José Maria, Luiz Gonzaga, André Ruperto

---

**Ambiente**: Desenvolvimento Local  
**Atualizado**: Janeiro 2025  
**ChatCOTIN**: Versão 2.0 - Modelos Otimizados 