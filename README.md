# Chatbot Django com Databricks Llama 4 Maverick

Um chatbot inteligente desenvolvido em Django que utiliza o modelo **Databricks Llama 4 Maverick** para responder perguntas sobre programação Python.

## 🚀 Características

- Interface web moderna e responsiva
- Sistema de autenticação de usuários
- Histórico de conversas persistente
- Respostas em formato Markdown
- Integração com Databricks Llama 4 Maverick
- Suporte a contexto de conversação

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.1.3
- **LLM**: Databricks Llama 4 Maverick
- **Framework LLM**: Databricks LangChain
- **Banco de Dados**: SQLite (desenvolvimento)
- **Frontend**: HTML, CSS, JavaScript
- **Autenticação**: Django Auth

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Databricks
- Token de acesso do Databricks
- Acesso ao modelo Llama 4 Maverick

## ⚙️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd ia_code_assistance
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Configure as variáveis de ambiente
Edite o arquivo `.env` na raiz do projeto:

```env
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=seu-token-aqui
DATABRICKS_MODEL_ENDPOINT=databricks-llama-4-maverick
```

### 4. Execute o script de migração
```bash
python migrate_to_databricks.py
```

Este script irá:
- Verificar as configurações do .env
- Instalar as dependências necessárias
- Testar a conexão com o Databricks

### 5. Configure o banco de dados
```bash
python manage.py migrate
```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor
```bash
python manage.py runserver
```

O aplicativo estará disponível em `http://localhost:8000`

## 📖 Como Usar

1. **Registro/Login**: Crie uma conta ou faça login
2. **Chat**: Digite suas perguntas sobre programação Python
3. **Histórico**: Visualize suas conversas anteriores
4. **Contexto**: O chatbot mantém o contexto da conversa

## 🔧 Configuração do Databricks

Para configurar o Databricks corretamente, consulte o arquivo `DATABRICKS_SETUP.md` que contém instruções detalhadas sobre:

- Como obter credenciais do Databricks
- Configuração de tokens de acesso
- Configuração de endpoints de modelo
- Troubleshooting comum

## 📁 Estrutura do Projeto

```
ia_code_assistance/
├── core/                   # Configurações do Django
│   ├── settings.py        # Configurações principais
│   ├── urls.py           # URLs principais
│   └── templates/        # Templates base
├── chatbot/              # App do chatbot
│   ├── models.py        # Modelos de dados
│   ├── views.py         # Lógica de negócio
│   └── urls.py          # URLs do chatbot
├── accounts/            # App de autenticação
├── requirements.txt     # Dependências Python
├── .env                # Variáveis de ambiente
└── manage.py           # Script de gerenciamento Django
```

## 🔄 Migração do Groq

Este projeto foi migrado do Groq para o Databricks. As principais mudanças incluem:

- **Autenticação**: Token Databricks em vez de API key Groq
- **Modelo**: Databricks Llama 4 Maverick
- **Dependências**: `databricks-langchain` e `databricks-sdk`
- **Configuração**: Workspace e endpoint Databricks

## 🐛 Troubleshooting

### Erro de Autenticação
- Verifique se o token Databricks está correto
- Confirme se o workspace URL está correto
- Certifique-se de que o token não expirou

### Erro de Modelo
- Verifique se o endpoint do modelo existe
- Confirme se você tem permissão para acessar o modelo
- Teste a conectividade com o Databricks

### Problemas de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🤝 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Consulte o arquivo `DATABRICKS_SETUP.md`
2. Execute o script `migrate_to_databricks.py`
3. Verifique os logs de erro do Django
4. Abra uma issue no repositório 