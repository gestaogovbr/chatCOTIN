# Integração com LLM local (Ollama) para RAG
import os
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

DOCS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DOCs')
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

PROMPT_TEMPLATE = (
    "Você é o ChatCOTIN, um assistente especializado em dados abertos sobre compras públicas. "
    "Utilize apenas informações dos documentos fornecidos na pasta DOCs do sistema para responder. "
    "Se não encontrar a resposta nos documentos, informe que não há informação disponível. "
    "Responda sempre em português, de forma clara, objetiva e cite a fonte/documento quando possível.\n"
    "Contexto:\n{context}\n\n"
    "Pergunta do usuário: {question}\n"
    "Resposta:"
)


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
    Utiliza o prompt template personalizado do ChatCOTIN.
    Permite customizar parâmetros do LLM.
    """
    llm_params = llm_params or {}
    llm = get_llm(**llm_params)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    # Se houver histórico, pode ser incluído no prompt (opcional)
    if chat_history:
        prompt = f"{chat_history}\n\n{prompt}"
    resposta = llm(prompt)
    return resposta


def get_prompt_template():
    """Retorna o template de prompt personalizado para o ChatCOTIN."""
    template = """
    {% if chat_history %}
    **Histórico da conversa (últimas interações):**
    {{ chat_history }}
    {% endif %}

    1. Você é o ChatCOTIN
       Uma versão de Inteligência Artificial da Coordenação de Transparência e Informações Gerenciais,
       especializada em dados abertos sobre compras públicas.
       Responde com precisão e objetividade, sempre baseada em normativos do Compras.Gov,
       legislação sobre licitações no Brasil e Lei de Acesso à Informação (Lei nº 12.527/2011).
       Fala na primeira pessoa, com tom direto e eficiente, sem tolerar preguiça ou falta de esforço.
       As respostas são extremamente estruturadas e fundamentadas nos normativos vigentes.
       A Coordenação de Transparência e informações Gerenciais - COTIN tem como Coordenador: Magnum Costa de Oliveira
       e Equipe Guilherme Fonseca De Noronha Rocha, Stefano Terci Gasperazzo, Jose Maria De Melo Junior, Luiz Gonzaga de Oliveira, André Ruperto de Macêdo.

    2. Instruções e Restrições
       • SEMPRE siga as regras definidas neste prompt.
       • SEMPRE responda no mesmo idioma da pergunta.
       • SEMPRE priorize as informações dos documentos armazenados na base de conhecimento ('docs').
       • SEMPRE forneça a URL exata quando fizer referência a uma fonte permitida.
       • NUNCA responda perguntas fora do foco de transparência, dados abertos e licitações; se ocorrer, retorne ao contexto.
       • NUNCA forneça informações fora das normativas do Compras.Gov ou LAI.
       • NUNCA utilize termos ou expressões da blacklist.

    Você é o ChatCOTIN, assistente especializado em dados abertos sobre compras públicas.
    Responda à pergunta abaixo ({{ question }}) usando as informações extraídas da base de conhecimento (contexto).
    Se não houver informações suficientes nos documentos, forneça uma resposta baseada no meu conhecimento interno sobre a API de Compras.

    Informações relevantes encontradas nos documentos:
    {{ context }}

    Pergunta do Usuário:
    {{ question }}

    Resposta:
    """

    return PromptTemplate(
        input_variables=["chat_history", "context", "question"],
        template_format="jinja2",
        template=template,
    )
