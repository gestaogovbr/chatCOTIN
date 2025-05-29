import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from databricks_langchain import ChatDatabricks
from markdown import markdown

from chatbot.models import Chat
from chatbot.vectorstore import semantic_search, filter_relevant_documents, get_vectorstore
from chatbot.llm import generate_answer


# Configuração das variáveis de ambiente do Databricks
os.environ['DATABRICKS_HOST'] = settings.DATABRICKS_HOST
os.environ['DATABRICKS_TOKEN'] = settings.DATABRICKS_TOKEN


MAX_HISTORY = 6  # Número máximo de interações a serem consideradas no contexto


def get_chat_history(chats):
    chat_history = []
    for chat in chats:
        chat_history.append(
            ('human', chat.message,)
        )
        chat_history.append(
            ('ai', chat.response,)
        )
    return chat_history


def ask_ai(context, message):
    model = ChatDatabricks(
        endpoint=settings.DATABRICKS_MODEL_ENDPOINT,
        temperature=0.7,
        max_tokens=2048
    )
    messages = [
        (
            'system',
            'Você é o ChatCOTIN, um assistente especializado em dados abertos e transparência pública sobre compras governamentais. '
            'Responda sempre em português, de forma clara, objetiva e cite a fonte/documento quando possível. '
            'Utilize apenas informações dos documentos fornecidos na pasta DOCs do sistema para responder. '
            'Se não encontrar a resposta nos documentos, informe que não há informação disponível. Responda em formato markdown.'
        ),
    ]
    messages.extend(context)
    messages.append(
        (
            'human',
            message,
        ),
    )
    print(messages)
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')


def ask_rag_local(message, k=5, llm_params=None, chat_history=None):
    """Pipeline RAG: busca contexto relevante e gera resposta usando LLM local (Ollama), com filtro avançado."""
    # Busca semântica inicial
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(message, k=10)
    # Filtro avançado de relevância
    embeddings = vectorstore._embedding_function
    relevant_docs = filter_relevant_documents(message, docs, embeddings, top_n=k)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    # Geração de resposta
    resposta = generate_answer(context, message, chat_history=chat_history, llm_params=llm_params)
    return resposta


def build_chat_history(chats, max_history=MAX_HISTORY):
    """
    Monta o histórico de conversação limitado para o prompt do LLM.
    Se houver mais interações, sumariza as mais antigas.
    """
    if not chats:
        return ""
    # Se houver poucas interações, retorna todas
    if len(chats) <= max_history:
        return "\n".join([
            f"Usuário: {c.message}\nAssistente: {c.response}" for c in chats
        ])
    # Sumariza as mais antigas e mantém as últimas max_history-1 completas
    old_chats = chats[:-max_history+1]
    recent_chats = chats[-max_history+1:]
    # Sumarização simples: só as perguntas e respostas principais
    summary = f"Resumo das interações anteriores: {len(old_chats)} trocas."
    # (Opcional: implementar sumarização real com LLM ou heurística)
    history = [summary]
    history += [f"Usuário: {c.message}\nAssistente: {c.response}" for c in recent_chats]
    return "\n".join(history)


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        llm_provider = request.POST.get('llm_provider', getattr(settings, 'LLM_PROVIDER', 'databricks'))
        llm_params = {}
        for param in ["temperature", "top_p", "top_k", "num_ctx", "repeat_penalty"]:
            value = request.POST.get(param)
            if value is not None:
                try:
                    llm_params[param] = float(value) if "." in value else int(value)
                except ValueError:
                    pass
        # Usa histórico controlado
        chat_history = build_chat_history(list(chats.order_by('id')))
        if llm_provider == 'ollama':
            response = ask_rag_local(message, llm_params=llm_params, chat_history=chat_history)
        else:
            context = get_chat_history(chats=chats)
            response = ask_ai(context=context, message=message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
        )
        chat.save()

        return JsonResponse({
            'message': message,
            'response': response,
        })
    return render(request, 'chatbot_new.html', {'chats': chats})


@login_required
def clear_history(request):
    if request.method == 'POST':
        try:
            # Delete all chats for the current user
            Chat.objects.filter(user=request.user).delete()
            return JsonResponse({'success': True, 'message': 'Histórico limpo com sucesso'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
