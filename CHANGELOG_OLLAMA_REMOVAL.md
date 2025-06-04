# Changelog - Remoção do Modelo Ollama

## Data: Janeiro 2025

### Resumo das Alterações

O modelo Ollama (llama3.2:latest) foi removido do ChatCOTIN, mantendo apenas os modelos Databricks e Groq Cloud. Esta decisão foi tomada para simplificar a arquitetura e focar nos modelos em nuvem que oferecem melhor performance e escalabilidade.

---

## Alterações Realizadas

### 1. **Arquivo: `chatbot/llm.py`**

**Removido:**
- Importação `from langchain_ollama import OllamaLLM`
- Importação `from langchain.prompts import PromptTemplate`
- Variáveis `OLLAMA_BASE_URL` e `OLLAMA_MODEL`
- Função `get_llm()` (configuração do Ollama)
- Função `generate_answer()` (geração via Ollama)

**Mantido:**
- Template unificado `UNIFIED_PROMPT_TEMPLATE`
- Função `get_unified_prompt_template()`
- Função `get_groq_llm()`
- Função `generate_answer_groq()`

### 2. **Arquivo: `chatbot/views.py`**

**Removido:**
- Importação `generate_answer` do `llm.py`
- Função `ask_rag_local()` (pipeline RAG para Ollama)
- Lógica de parâmetros LLM customizáveis
- Condicionais para `llm_provider == 'ollama'`

**Atualizado:**
- Simplificada lógica de seleção de modelo
- Databricks definido como padrão
- Função `regenerate_response()` atualizada

### 3. **Arquivo: `core/templates/chatbot_new.html`**

**Removido:**
- Radio button para modelo Ollama
- Seção completa de "Parâmetros do Modelo (Ollama)"
- Campos: temperature, top-p, top-k, contexto, repeat penalty
- Lógica JavaScript para parâmetros LLM
- Funções de carregamento/salvamento de parâmetros LLM

**Atualizado:**
- Databricks marcado como padrão (`checked`)
- JavaScript simplificado sem referências aos parâmetros Ollama

### 4. **Arquivo: `requirements.txt`**

**Removido:**
- Dependência `langchain-ollama`

**Mantido:**
- Todas as outras dependências intactas

---

## Modelos Disponíveis Após a Alteração

1. **databricks-llama-4-maverick (Padrão)**
   - Modelo em nuvem via Databricks
   - Configurado nas variáveis de ambiente
   - Melhor para uso em produção

2. **llama-3.3-70b-versatile (Groq Cloud)**
   - Modelo de alta performance via Groq
   - 70B parâmetros
   - Configurado via `GROQ_API_KEY`

---

## Funcionalidades Mantidas

✅ **Sistema RAG completo**
- Busca semântica
- Filtro de relevância
- Busca especializada para painéis

✅ **Gestão de conversas**
- Histórico de conversas
- Sidebar com navegação
- Busca em conversas

✅ **Interface e UX**
- Design Gov.br
- Responsividade
- Feedback de usuário

✅ **Prompts unificados**
- Template único para todos os modelos
- Identidade ChatCOTIN preservada
- Instruções especializadas mantidas

---

## Benefícios da Alteração

1. **Simplificação da Arquitetura**
   - Menos dependências para gerenciar
   - Código mais limpo e mantível
   - Menos pontos de falha

2. **Foco em Modelos em Nuvem**
   - Melhor performance
   - Maior disponibilidade
   - Escalabilidade automática

3. **Redução de Complexidade**
   - Menos parâmetros para configurar
   - Interface mais simples
   - Onboarding facilitado

---

## Impactos

### ✅ **Sem Impacto**
- Usuários existentes
- Dados históricos
- Funcionalidades RAG
- Qualidade das respostas

### ⚠️ **Requer Atenção**
- Usuários que tinham Ollama como padrão migrarão automaticamente para Databricks
- Configurações de parâmetros LLM personalizados foram resetadas

---

## Próximos Passos Recomendados

1. **Teste em Ambiente de Desenvolvimento**
   ```bash
   # Instalar dependências atualizadas
   pip install -r requirements.txt
   
   # Testar ambos os modelos
   # Verificar se GROQ_API_KEY está configurada
   ```

2. **Deploy em Produção**
   - Verificar configurações Databricks
   - Confirmar chave Groq ativa
   - Monitorar logs iniciais

3. **Comunicação com Usuários**
   - Informar sobre simplificação
   - Destacar modelos mais potentes disponíveis

---

## Contato Técnico

Para dúvidas sobre essas alterações:
- **Equipe COTIN**: Coordenação de Transparência e Informações Gerenciais
- **Coordenador**: Magnum Costa de Oliveira
- **Desenvolvedores**: Guilherme Fonseca, Stefano Terci, José Maria, Luiz Gonzaga, André Ruperto

---

*Documento criado em: Janeiro 2025*
*ChatCOTIN - Versão 2.0 - Modelos Otimizados* 