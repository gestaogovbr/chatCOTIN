# 🚀 Guia de Deploy para Azure - DevOps Team

## 📋 **Resumo da Aplicação**
- **Framework**: Django 5.1.3
- **Linguagem**: Python 3.8+
- **Banco**: PostgreSQL (recomendado para produção)
- **LLM**: Databricks Llama 4 Maverick
- **Arquivos Estáticos**: WhiteNoise (self-contained)

## 🔧 **Pré-requisitos Azure**

### **Serviços Necessários:**
1. **Azure App Service** (ou Container Instance)
2. **Azure Database for PostgreSQL**
3. **Azure Key Vault** (para secrets)
4. **Azure Application Insights** (monitoramento)

### **Variáveis de Ambiente Obrigatórias:**
```bash
# Core Django
DEBUG=False
SECRET_KEY=<gerar-key-50-chars-minimo>
ALLOWED_HOSTS=<dominio-azure>.azurewebsites.net,<dominio-custom>

# Database
DATABASE_URL=postgres://user:pass@host:port/dbname

# Databricks (fornecido pelo time de negócio)
DATABRICKS_HOST=https://workspace.cloud.databricks.com
DATABRICKS_TOKEN=<token-databricks>
DATABRICKS_MODEL_ENDPOINT=databricks-llama-4-maverick
```

## 🏗️ **Configuração de Deploy**

### **1. Azure App Service Settings:**
```json
{
  "pythonVersion": "3.11",
  "startupCommand": "gunicorn core.wsgi:application --bind 0.0.0.0:8000",
  "appSettings": {
    "SCM_DO_BUILD_DURING_DEPLOYMENT": "1",
    "WEBSITE_HTTPLOGGING_RETENTION_DAYS": "3"
  }
}
```

### **2. Comandos de Inicialização:**
```bash
# Durante o deploy, executar:
python manage.py collectstatic --noinput
python manage.py migrate
```

### **3. Health Check Endpoint:**
- **URL**: `/health/` (implementado na aplicação)
- **Método**: GET
- **Resposta**: HTTP 200 + JSON status

## 🗄️ **Configuração de Banco de Dados**

### **Azure PostgreSQL:**
```bash
# String de conexão recomendada:
DATABASE_URL=postgres://username:password@servername.postgres.database.azure.com:5432/database_name?sslmode=require

# Configurações mínimas recomendadas:
- vCores: 2
- Storage: 20GB
- Backup retention: 7 days
```

### **Migrações Iniciais:**
```bash
# Executar após primeiro deploy:
python manage.py migrate
python manage.py createsuperuser  # Opcional
```

## 🔒 **Configurações de Segurança**

### **Headers de Segurança (já configurados no código):**
- HSTS ativado
- XSS Protection
- Content Type Nosniff
- SSL Redirect (em produção)

### **Secrets no Azure Key Vault:**
```bash
# Recomendado armazenar no Key Vault:
- SECRET_KEY
- DATABASE_URL
- DATABRICKS_TOKEN
```

## 📊 **Monitoramento e Logs**

### **Application Insights:**
- Configurar instrumentação automática
- Monitorar requests para `/chatbot/`
- Alertas para erros de Databricks

### **Logs Importantes:**
```bash
# Paths para monitorar:
/var/log/django.log
/var/log/gunicorn.log

# Endpoints críticos:
GET /health/
POST /chatbot/message/
GET /accounts/login/
```

## 🚀 **Processo de Deploy Recomendado**

### **1. Deploy Inicial:**
```bash
1. Criar App Service
2. Configurar PostgreSQL
3. Configurar variáveis de ambiente
4. Deploy do código
5. Executar migrações
6. Testar endpoints principais
```

### **2. Deploy Contínuo:**
```bash
1. Configurar GitHub Actions (arquivo já presente)
2. Branch main → deploy automático
3. Testes automáticos antes do deploy
```

## 🧪 **Testes Pós-Deploy**

### **Checklist de Validação:**
- [ ] `/health/` retorna 200
- [ ] `/admin/` acessível
- [ ] `/accounts/login/` funcional
- [ ] `/chatbot/` carrega corretamente
- [ ] Teste de mensagem no chatbot
- [ ] Verificar logs do Databricks

### **URLs para Testar:**
```bash
GET  /health/
GET  /admin/
GET  /accounts/login/
POST /chatbot/message/ (com autenticação)
GET  /static/admin/css/base.css
```

## ⚠️ **Troubleshooting Comum**

### **Erro de Static Files:**
```bash
# Solução: Executar collectstatic
python manage.py collectstatic --noinput
```

### **Erro de Database:**
```bash
# Verificar: String de conexão
# Verificar: Firewall do PostgreSQL
# Executar: python manage.py migrate
```

### **Erro do Databricks:**
```bash
# Verificar: Token válido
# Verificar: Endpoint correto
# Verificar: Conectividade de rede
```

## 📞 **Contato para Suporte**
- **Desenvolvedor**: [Seu contato]
- **Databricks**: [Contato do time de AI]
- **Documentação**: README.md e DATABRICKS_SETUP.md 