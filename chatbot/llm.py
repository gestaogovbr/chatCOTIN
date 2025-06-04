# Integração com modelos de IA para RAG - ChatCOTIN
import os
from groq import Groq
from markdown import markdown
from django.conf import settings

# Configuração do Groq - usar Django settings
GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', '')

DOCS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Docs')
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

# Template de prompt unificado e otimizado para modelos de IA
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


def get_unified_prompt_template():
    """Retorna o template de prompt unificado para o ChatCOTIN (compatível com todos os modelos)."""
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
    Inclui proteção contra contexto muito longo e retry em caso de erro 503.
    """
    client = get_groq_llm()
    
    # Proteção contra contexto muito longo (Groq tem limite de ~128K tokens)
    # Estimativa: 1 token ≈ 4 caracteres em português
    MAX_CONTEXT_CHARS = 80000  # ~20K tokens para contexto
    MAX_HISTORY_CHARS = 8000   # ~2K tokens para histórico
    
    # Truncar contexto se muito longo
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n\n[CONTEXTO TRUNCADO DEVIDO AO TAMANHO]"
        print(f"⚠️ Contexto truncado para {MAX_CONTEXT_CHARS} caracteres")
    
    # Truncar histórico se muito longo
    if chat_history and len(chat_history) > MAX_HISTORY_CHARS:
        chat_history = chat_history[-MAX_HISTORY_CHARS:] + "\n[HISTÓRICO TRUNCADO]"
        print(f"⚠️ Histórico truncado para {MAX_HISTORY_CHARS} caracteres")
    
    # Usar o template unificado
    prompt = UNIFIED_PROMPT_TEMPLATE.format(context=context, question=question)
    
    # Se houver histórico, incluir no prompt
    if chat_history:
        prompt = f"HISTÓRICO DA CONVERSA:\n{chat_history}\n\n{prompt}"
    
    # Implementar retry para erro 503 (Service Unavailable)
    import time
    max_retries = 3
    
    for attempt in range(max_retries):
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
            error_str = str(e)
            
            # Se for erro 503 e ainda há tentativas, retry com delay
            if '503' in error_str and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # 2s, 4s, 6s
                print(f"⚠️ Erro 503 (tentativa {attempt + 1}/{max_retries}). Tentando novamente em {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            # Se for erro de token limit, tentar com contexto ainda menor
            elif ('token' in error_str.lower() or 'length' in error_str.lower()) and attempt == 0:
                print("⚠️ Erro de token limit. Reduzindo contexto...")
                context = context[:40000] + "\n\n[CONTEXTO REDUZIDO DEVIDO A LIMITE DE TOKENS]"
                prompt = UNIFIED_PROMPT_TEMPLATE.format(context=context, question=question)
                if chat_history:
                    prompt = f"HISTÓRICO DA CONVERSA:\n{chat_history[:4000]}\n\n{prompt}"
                continue
            
            # Para outros erros ou esgotadas as tentativas
            else:
                # Melhorar mensagem de erro para o usuário
                if '503' in error_str:
                    return ("⚠️ O serviço Groq está temporariamente indisponível devido a alta demanda. "
                           "Por favor, tente novamente em alguns minutos ou use o modelo Databricks.")
                elif '401' in error_str:
                    return "❌ Erro de autenticação com Groq. Verifique a configuração da API key."
                elif '429' in error_str:
                    return ("⚠️ Limite de requisições excedido. Aguarde alguns minutos antes de tentar novamente "
                           "ou use o modelo Databricks.")
                else:
                    return f"❌ Erro inesperado: {error_str}"
    
    # Se chegou aqui, todas as tentativas falharam
    return ("⚠️ Não foi possível conectar ao Groq após várias tentativas. "
           "Por favor, tente usar o modelo Databricks ou tente novamente mais tarde.")
