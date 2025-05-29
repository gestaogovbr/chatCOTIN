<div align="center">

![Logo ChatCOTIN](core/static/img/logo_cotin.png)

# ChatCOTIN
## Assistente Inteligente de Dados Abertos sobre Compras Públicas

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1.3-darkgreen?logo=django&logoColor=white)](https://djangoproject.com)
[![Licença](https://img.shields.io/badge/Licença-Gov.br-blue)](LICENSE)

**ChatCOTIN** é uma solução inovadora desenvolvida pela **Coordenação de Transparência e Informações Gerenciais (COTIN/CGGES/DELOG)** para facilitar o acesso e compreensão de dados abertos sobre compras públicas federais.

</div>

---

## 🎯 **Sobre o Projeto**

O ChatCOTIN é um assistente virtual inteligente especializado em transparência pública, que combina tecnologias de Inteligência Artificial com a rica base de conhecimento sobre compras governamentais. Nosso objetivo é democratizar o acesso às informações públicas, promovendo transparência, eficiência e inovação no setor público.

### 🏛️ **Equipe Responsável**

- **Coordenador**: Magnum Costa de Oliveira
- **Equipe de Desenvolvimento**:
  - Guilherme Fonseca De Noronha Rocha
  - Stefano Terci Gasperazzo
  - Jose Maria De Melo Junior
  - Luiz Gonzaga de Oliveira
  - Flávio Henrique Martins

---

## ✨ **Principais Características**

### 🧠 **Inteligência Artificial Especializada**
- Sistema RAG (Retrieval-Augmented Generation) para respostas precisas
- Base de conhecimento especializada em compras públicas
- Suporte aos modelos em Nuvem e local
- Processamento de linguagem natural em português brasileiro

### 🔍 **Áreas de Especialização**
- **API de Dados Abertos** do Governo Federal
- **Portal Compras.gov.br** e suas funcionalidades
- **Lei de Acesso à Informação** (Lei 12.527/2011)
- **Painel de Compras Governamentais**
- **Portal Nacional de Contratações Públicas (PNCP)**
- **Módulos de Transparência Ativa**

### 🛠️ **Funcionalidades Técnicas**
- Interface web moderna e responsiva
- Sistema de autenticação seguro
- Histórico de conversas persistente
- Suporte a markdown nas respostas
- Busca semântica inteligente
- Base de conhecimento atualizável

---

## 🚀 **Tecnologias Utilizadas**

### **Backend**
- **Django 5.1.3** - Framework web robusto
- **Python 3.12+** - Linguagem de programação
- **LangChain** - Framework para LLM
- **ChromaDB** - Banco vetorial para embeddings
- **WhiteNoise** - Servir arquivos estáticos

### **Inteligência Artificial**
- **Databricks** - LLM em nuvem (produção)
- **Ollama** - LLM local (desenvolvimento)
- **Sentence Transformers** - Embeddings multilíngues
- **RAG (Retrieval-Augmented Generation)** - Sistema de busca inteligente

### **Frontend**
- **HTML5/CSS3** - Interface moderna
- **JavaScript ES6+** - Interatividade
- **Bootstrap 5** - Framework CSS responsivo
- **Font Awesome** - Ícones profissionais
- **Marked.js** - Renderização de Markdown

### **Banco de Dados**
- **SQLite** - Desenvolvimento local
- **PostgreSQL** - Produção (Azure)

---

## 📋 **Pré-requisitos**

- **Python 3.12+** instalado
- **Git** para controle de versão
- **Conta Databricks** (para produção) ou **Ollama** (para desenvolvimento)

---

## ⚙️ **Instalação e Configuração**

### **1. Clone o Repositório**
```bash
git clone https://github.com/gestaogovbr/chatCOTIN.git
cd chatCOTIN
```

### **2. Configure o Ambiente Virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### **3. Instale as Dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **4. Configure as Variáveis de Ambiente**
Copie o arquivo `.env.example` para `.env` e configure:

```env
# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Databricks (Produção)
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=seu-token-aqui
DATABRICKS_MODEL_ENDPOINT=seu-endpoint-aqui

# Ollama (Desenvolvimento)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

### **5. Configure o Banco de Dados**
```bash
python manage.py migrate
python manage.py createsuperuser  # (opcional)
```

### **6. Atualize a Base de Conhecimento**
```bash
python atualizar_base_conhecimento.py
```

### **7. Execute o Servidor**
```bash
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

## 📁 **Estrutura do Projeto**

```
chatCOTIN/
├── 📂 accounts/              # Autenticação de usuários
├── 📂 chatbot/               # Core do sistema de chat
│   ├── llm.py               # Integração com LLMs
│   ├── vectorstore.py       # Gerenciamento de embeddings
│   ├── models.py            # Modelos de dados
│   └── views.py             # Lógica de negócio
├── 📂 core/                  # Configurações do Django
│   ├── static/              # Arquivos estáticos
│   │   └── img/
│   │       └── logo_cotin.png
│   ├── templates/           # Templates HTML
│   └── settings.py          # Configurações
├── 📂 Docs/                  # Base de conhecimento
├── 📂 chroma_db/             # Banco vetorial
├── 📄 requirements.txt       # Dependências Python
├── 📄 atualizar_base_conhecimento.py  # Script de atualização
├── 📄 SETUP_DESENVOLVIMENTO.md        # Guia desenvolvimento
├── 📄 DEPLOY_AZURE.md                 # Guia deploy Azure
└── 📄 manage.py             # Gerenciador Django
```

---

## 🔄 **Como Atualizar a Base de Conhecimento**

O ChatCOTIN utiliza RAG para fornecer respostas baseadas em documentos oficiais. Para adicionar novos documentos:

1. **Adicione documentos** na pasta `Docs/` (formatos: `.docx`, `.md`, `.txt`)
2. **Execute o script**: `python atualizar_base_conhecimento.py`
3. **Aguarde o processamento** e teste as novas informações

Consulte o guia completo: [`COMO_ATUALIZAR_BASE_CONHECIMENTO.md`](COMO_ATUALIZAR_BASE_CONHECIMENTO.md)

---

## 🌐 **Deploy em Produção**

### **Azure App Service (Recomendado)**

O projeto está otimizado para deploy no Azure. Consulte o guia detalhado:
- 📖 **Guia Completo**: [`DEPLOY_AZURE.md`](DEPLOY_AZURE.md)
- 🔧 **Script de Inicialização**: [`startup.sh`](startup.sh)
- ✅ **Checklist de Deploy**: `python manage.py check_deployment`

### **Endpoints de Monitoramento**
- **Health Check**: `/health/` - Status da aplicação
- **Status Detalhado**: `/status/` - Informações do sistema
- **Painel Admin**: `/admin/` - Administração

---

## 📖 **Documentação Adicional**

- 🛠️ **[Guia de Desenvolvimento](SETUP_DESENVOLVIMENTO.md)** - Setup completo para desenvolvedores
- 🔄 **[Atualização da Base](COMO_ATUALIZAR_BASE_CONHECIMENTO.md)** - Como incluir novos documentos
- ☁️ **[Deploy Azure](DEPLOY_AZURE.md)** - Guia para DevOps
- 🐧 **[Produção Ollama](OLLAMA_PRODUCTION_GUIDE.md)** - Setup Ollama em produção

---

## 🔍 **Módulos da API Suportados**

O ChatCOTIN tem conhecimento especializado sobre:

- **CATÁLOGO MATERIAL** - Materiais do governo
- **CATÁLOGO SERVIÇO** - Serviços contratados  
- **PESQUISA DE PREÇO** - Valores e preços
- **PGC** - Planejamento e Gerenciamento
- **UASG** - Unidades Administrativas
- **CONTRATOS** - Gestão de contratos
- **ARP** - Atas de Registro de Preço
- **LEGADO** - Licitações Lei 8.666/93
- **CONTRATAÇÕES** - Nova Lei 14.133/2021

---

## 🤝 **Contribuição**

O ChatCOTIN é um projeto do Governo Federal brasileiro. Para contribuições:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Faça um push para a branch
5. Abra um Pull Request

---

## 📞 **Suporte e Contato**

- **Instituição**: Ministério da Gestão e da Inovação em Serviços Públicos
- **Coordenação**: COTIN/CGGES/DELOG
- **E-mail**: [cgges.delog@gestao.gov.br](mailto:cgges.delog.delog@gestao.gov.br)
- **Portal**: [Compras.gov.br](https://compras.gov.br)

---

## 📄 **Licença**

Este projeto está sob a licença do Governo Brasileiro. Consulte os termos de uso do [Portal de Software Público Brasileiro](https://www.gov.br/governodigital/pt-br/software-publico-brasileiro).

---

## 🌟 **Reconhecimentos**

Agradecemos a todos os servidores públicos e desenvolvedores que contribuem para a transparência e inovação no setor público brasileiro.

---

<div align="center">

**[🚀 Acesse o ChatCOTIN](https://chatcotin.gov.br)** | **[📊 Portal Compras](https://compras.gov.br)** | **[🏛️ Gov.br](https://www.gov.br)**

---

*Desenvolvido com ❤️ pela equipe COTIN - Promovendo transparência através da tecnologia*

</div> 