# Configuração do Databricks Llama 4 Maverick

Este projeto foi migrado para usar o modelo **Databricks Llama 4 Maverick** em vez do Groq.

## Configuração Necessária

### 1. Obter Credenciais do Databricks

Você precisa ter:
- Uma conta no Databricks
- Acesso ao workspace do Databricks
- Um token de acesso pessoal (Personal Access Token)

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` na raiz do projeto e configure as seguintes variáveis:

```env
DATABRICKS_HOST=https://seu-workspace.cloud.databricks.com
DATABRICKS_TOKEN=seu-token-aqui
DATABRICKS_MODEL_ENDPOINT=databricks-llama-4-maverick
```

**Importante:** 
- Substitua `seu-workspace.cloud.databricks.com` pela URL do seu workspace Databricks
- Substitua `seu-token-aqui` pelo seu token de acesso pessoal
- O endpoint do modelo pode variar dependendo da sua configuração

### 3. Como Obter o Token de Acesso

1. Faça login no seu workspace Databricks
2. Clique no seu avatar no canto superior direito
3. Selecione "User Settings"
4. Vá para a aba "Access tokens"
5. Clique em "Generate new token"
6. Dê um nome ao token e defina um tempo de expiração
7. Copie o token gerado (você só verá ele uma vez!)

### 4. Configurar o Endpoint do Modelo

O endpoint do modelo pode ser:
- Um endpoint de serving model que você criou
- Um endpoint de foundation model disponível no seu workspace

Para verificar os endpoints disponíveis:
1. No Databricks, vá para "Serving"
2. Verifique os endpoints disponíveis
3. Use o nome do endpoint na variável `DATABRICKS_MODEL_ENDPOINT`

### 5. Instalar Dependências

Execute o comando para instalar as novas dependências:

```bash
pip install -r requirements.txt
```

### 6. Testar a Configuração

Após configurar tudo, execute o servidor Django:

```bash
python manage.py runserver
```

E teste o chatbot para verificar se está funcionando com o novo modelo.

## Diferenças do Groq

- **Autenticação**: Agora usa token do Databricks em vez de API key do Groq
- **Modelo**: Usa Databricks Llama 4 Maverick em vez de llama-3.2-90b-text-preview
- **Configuração**: Requer configuração de workspace e endpoint
- **Dependências**: Usa `databricks-langchain` e `databricks-sdk`

## Troubleshooting

### Erro de Autenticação
- Verifique se o token está correto
- Verifique se o host do workspace está correto
- Certifique-se de que o token não expirou

### Erro de Endpoint
- Verifique se o endpoint do modelo existe
- Verifique se você tem permissão para acessar o endpoint
- Confirme o nome exato do endpoint no Databricks

### Erro de Dependências
- Execute `pip install -r requirements.txt` novamente
- Verifique se está usando o ambiente virtual correto 