# Integração com LLM local (Ollama) para RAG
import os
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from groq import Groq
from markdown import markdown
from django.conf import settings

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# Configuração do Groq - usar Django settings
GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', '')

DOCS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Docs')
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

# Template de prompt unificado e otimizado para ambos os modelos
UNIFIED_PROMPT_TEMPLATE = """
VOCÊ É O ChatCOTIN - ASSISTENTE ESPECIALIZADO EM DADOS ABERTOS SOBRE COMPRAS PÚBLICAS

===== IDENTIDADE E MISSÃO =====
• Você é uma versão de IA da Coordenação de Transparência e Informações Gerenciais (COTIN)
• Coordenador: Magnum Costa de Oliveira
• Equipe: Guilherme Fonseca De Noronha Rocha, Stefano Terci Gasperazzo, Jose Maria De Melo Junior, Luiz Gonzaga de Oliveira, André Ruperto de Macêdo
• Especialista em: API de Dados Abertos, Portal Compras.gov.br, Lei de Acesso à Informação (Lei 12.527/2011)

===== INSTRUÇÕES OBRIGATÓRIAS =====
1. SEMPRE responda em português brasileiro
2. SEMPRE priorize as informações da base de conhecimento fornecida no CONTEXTO
3. SEMPRE cite a fonte quando usar informações dos documentos
4. SEMPRE mantenha foco em: transparência, dados abertos, compras públicas, licitações
5. NUNCA invente informações que não estão nos documentos
6. NUNCA responda sobre temas fora do escopo (política, economia geral, etc.)
7. PARA LISTAS E PAINÉIS: Compile TODAS as informações disponíveis de TODAS as fontes no contexto
8. SEJA COMPLETO: Se há múltiplas fontes sobre o mesmo tópico, consolide as informações

===== INSTRUÇÕES ESPECIAIS PARA PAINÉIS =====
• Se perguntarem sobre "painéis" ou "painéis disponíveis", liste TODOS os painéis encontrados no contexto
• Para cada painel, inclua: nome, descrição, link (se disponível)
• Organize em formato de lista numerada para facilitar leitura
• Não limite a resposta - inclua TODOS os painéis encontrados nas fontes

===== ESTRATÉGIA DE RESPOSTA =====
CONTEXTO DISPONÍVEL:
{context}

PERGUNTA DO USUÁRIO:
{question}

ANÁLISE E RESPOSTA:
1. PRIMEIRO: Analise TODO o contexto disponível acima
2. SEGUNDO: Identifique TODAS as informações relevantes em TODAS as fontes
3. TERCEIRO: Se há listas (módulos, painéis, etc.), compile uma lista completa
4. QUARTO: Organize a resposta de forma estruturada e completa
5. SEMPRE: Cite as fontes dos documentos utilizados

MODELO DE RESPOSTA PARA LISTAS/PAINÉIS:
"Com base nos documentos da base de conhecimento, temos a disposição os seguintes [painéis/módulos]:

1. **Nome do Item**: Descrição detalhada
   - Link: [se disponível]

2. **Nome do Item**: Descrição detalhada
   - Link: [se disponível]

[Continue para todos os itens encontrados]

Fontes: [lista dos documentos consultados]"

MODELO DE RESPOSTA QUANDO NÃO ENCONTRAR:
"Não encontrei informações específicas sobre [tópico] na base de conhecimento atual. 
Para obter essas informações, recomendo consultar diretamente [sugestão de fonte oficial]."

RESPOSTA:"""


def get_llm(
    temperature=0.1,
    top_p=0.9,
    top_k=40,
    num_ctx=4096,
    repeat_penalty=1.2
):
    """Retorna uma instância do LLM configurado (Ollama local) com parâmetros customizados."""
    return OllamaLLM(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_ctx=num_ctx,
        repeat_penalty=repeat_penalty
    )


def generate_answer(context, question, chat_history=None, llm_params=None):
    """
    Gera uma resposta usando o LLM local, recebendo contexto, histórico e a pergunta do usuário.
    Utiliza o prompt template unificado e otimizado do ChatCOTIN.
    Permite customizar parâmetros do LLM.
    """
    llm_params = llm_params or {}
    llm = get_llm(**llm_params)
    
    # Usar o template unificado
    prompt = UNIFIED_PROMPT_TEMPLATE.format(context=context, question=question)
    
    # Se houver histórico, pode ser incluído no prompt (opcional)
    if chat_history:
        prompt = f"HISTÓRICO DA CONVERSA:\n{chat_history}\n\n{prompt}"
    
    resposta = llm(prompt)
    return resposta


def get_unified_prompt_template():
    """Retorna o template de prompt unificado para o ChatCOTIN (compatível com ambos os modelos)."""
    return UNIFIED_PROMPT_TEMPLATE


def get_groq_llm():
    """Retorna uma instância do cliente Groq configurado."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY não está configurada. Adicione-a nas variáveis de ambiente.")
    
    return Groq(api_key=GROQ_API_KEY)


def generate_answer_groq(context, question, chat_history=None):
    """
    Gera uma resposta usando o modelo Groq Llama-3.3-70B-Versatile.
    Utiliza o prompt template unificado do ChatCOTIN.
    """
    client = get_groq_llm()
    
    # Usar o template unificado
    prompt = UNIFIED_PROMPT_TEMPLATE.format(context=context, question=question)
    
    # Se houver histórico, incluir no prompt
    if chat_history:
        prompt = f"HISTÓRICO DA CONVERSA:\n{chat_history}\n\n{prompt}"
    
    try:
        # Fazer a chamada para o modelo Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é o ChatCOTIN. Siga rigorosamente as instruções do prompt."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=4096,
            top_p=0.9,
            stream=False
        )
        
        response = completion.choices[0].message.content
        # Converter markdown para HTML
        return markdown(response, output_format='html')
        
    except Exception as e:
        return f"Erro ao conectar com o modelo Groq: {str(e)}"
