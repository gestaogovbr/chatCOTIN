import os
import json
from django.db.models import Q, Count
from django.core.paginator import Paginator

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from databricks_langchain import ChatDatabricks
from markdown import markdown

from chatbot.models import Chat, Conversation, ChatFeedback
from chatbot.vectorstore import semantic_search, filter_relevant_documents, get_vectorstore, enhanced_search_for_panels, is_panel_related_query
from chatbot.llm import generate_answer, get_unified_prompt_template


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
    
    # Buscar contexto relevante do RAG
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(message, k=10)
    embeddings = vectorstore._embedding_function
    relevant_docs = filter_relevant_documents(message, docs, embeddings, top_n=5)
    rag_context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Usar o template unificado
    unified_prompt = get_unified_prompt_template()
    
    # Aplicar o template unificado com contexto RAG
    prompt_content = unified_prompt.format(
        context=rag_context, 
        question=message
    )
    
    messages = [
        ('system', 'Você é o ChatCOTIN. Siga rigorosamente as instruções do prompt.'),
        ('human', prompt_content)
    ]
    
    print(messages)
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')


def ask_rag_local(message, k=5, llm_params=None, chat_history=None):
    """Pipeline RAG: busca contexto relevante e gera resposta usando LLM local (Ollama), com filtro avançado."""
    
    # Verificar se é uma consulta sobre painéis e usar busca especializada
    if is_panel_related_query(message):
        print("🎯 Consulta sobre painéis detectada - usando busca especializada")
        context_results = enhanced_search_for_panels(message, k=8)
        context = "\n\n".join(context_results)
    else:
        # Busca semântica normal
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
def chatbot(request, conversation_id=None):
    """View principal do chatbot - agora com suporte a conversas"""
    
    # Se conversation_id for fornecido, carregar conversa específica
    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        chats = conversation.chats.all()
        current_conversation = conversation
    else:
        # Buscar conversa ativa mais recente ou todas as mensagens (compatibilidade)
        current_conversation = Conversation.objects.filter(
            user=request.user, 
            is_active=True
        ).first()
        
        if current_conversation:
            chats = current_conversation.chats.all()
        else:
            # Fallback para chats antigos sem conversa
            chats = Chat.objects.filter(user=request.user, conversation__isnull=True)

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
        
        # Se não há conversa ativa, criar nova
        if not current_conversation:
            current_conversation = Conversation.objects.create(
                user=request.user,
                is_active=True
            )
        
        # Usar histórico da conversa atual
        conversation_chats = current_conversation.chats.all()
        chat_history = build_chat_history(list(conversation_chats.order_by('id')))
        
        if llm_provider == 'ollama':
            response = ask_rag_local(message, llm_params=llm_params, chat_history=chat_history)
        else:
            context = get_chat_history(chats=conversation_chats)
            response = ask_ai(context=context, message=message)

        # Criar novo chat associado à conversa
        chat = Chat(
            user=request.user,
            conversation=current_conversation,
            message=message,
            response=response,
        )
        chat.save()

        # Marcar conversa como ativa e atualizada
        current_conversation.is_active = True
        current_conversation.save()

        return JsonResponse({
            'message': message,
            'response': response,
            'conversation_id': current_conversation.id,
            'chat_id': chat.id,
        })
    
    return render(request, 'chatbot_new.html', {
        'chats': chats,
        'current_conversation': current_conversation,
    })


@login_required
def get_conversations_sidebar(request):
    """API para carregar dados da barra lateral"""
    try:
        conversations = Conversation.objects.filter(user=request.user).annotate(
            messages_count=Count('chats')
        ).order_by('-updated_at')
        
        # Organizar por grupos temporais
        grouped_conversations = {
            'today': [],
            'yesterday': [],
            'this_week': [],
            'older': []
        }
        
        for conversation in conversations:
            group = conversation.get_date_group()
            conversation_data = {
                'id': conversation.id,
                'title': conversation.title or 'Nova Conversa',
                'messages_count': conversation.messages_count,
                'updated_at': conversation.updated_at.isoformat(),
                'is_active': conversation.is_active,
            }
            grouped_conversations[group].append(conversation_data)
        
        return JsonResponse({
            'success': True,
            'conversations': grouped_conversations,
            'total_conversations': conversations.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def search_conversations(request):
    """API para buscar conversas"""
    try:
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({
                'success': False,
                'error': 'Query de busca não fornecida'
            }, status=400)
        
        # Buscar em conversas (título) e chats (mensagens)
        conversations = Conversation.objects.filter(
            Q(user=request.user) & (
                Q(title__icontains=query) |
                Q(chats__message__icontains=query) |
                Q(chats__response__icontains=query)
            )
        ).distinct().annotate(
            messages_count=Count('chats')
        ).order_by('-updated_at')
        
        results = []
        for conversation in conversations:
            # Buscar contexto da busca
            matching_chats = conversation.chats.filter(
                Q(message__icontains=query) | Q(response__icontains=query)
            )[:2]
            
            context_snippets = []
            for chat in matching_chats:
                if query.lower() in chat.message.lower():
                    context_snippets.append(f"Pergunta: {chat.message[:100]}...")
                if query.lower() in chat.response.lower():
                    context_snippets.append(f"Resposta: {chat.response[:100]}...")
            
            results.append({
                'id': conversation.id,
                'title': conversation.title or 'Nova Conversa',
                'messages_count': conversation.messages_count,
                'updated_at': conversation.updated_at.isoformat(),
                'context_snippets': context_snippets[:2],  # Máximo 2 snippets
            })
        
        return JsonResponse({
            'success': True,
            'results': results,
            'total_found': len(results),
            'query': query
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def new_conversation(request):
    """API para criar nova conversa"""
    try:
        if request.method == 'POST':
            # Desativar conversa atual
            Conversation.objects.filter(user=request.user, is_active=True).update(is_active=False)
            
            # Criar nova conversa
            new_conv = Conversation.objects.create(
                user=request.user,
                is_active=True
            )
            
            return JsonResponse({
                'success': True,
                'conversation_id': new_conv.id,
                'message': 'Nova conversa criada com sucesso'
            })
        
        return JsonResponse({
            'success': False,
            'error': 'Método não permitido'
        }, status=405)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def load_conversation(request, conversation_id):
    """API para carregar conversa específica"""
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        chats = conversation.chats.all().order_by('created_at')
        
        # Desativar outras conversas e ativar esta
        Conversation.objects.filter(user=request.user, is_active=True).update(is_active=False)
        conversation.is_active = True
        conversation.save()
        
        chat_data = []
        for chat in chats:
            chat_data.append({
                'id': chat.id,
                'message': chat.message,
                'response': chat.response,
                'created_at': chat.created_at.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'conversation': {
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at.isoformat(),
                'updated_at': conversation.updated_at.isoformat(),
            },
            'chats': chat_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def delete_conversation(request, conversation_id):
    """Deleta uma conversa"""
    if request.method == 'DELETE':
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
            conversation.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Conversa deletada com sucesso'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Erro ao deletar conversa: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


@login_required
def clear_history(request):
    """Limpar todo o histórico (mantido para compatibilidade)"""
    if request.method == 'POST':
        try:
            # Delete all conversations and chats for the current user
            Conversation.objects.filter(user=request.user).delete()
            Chat.objects.filter(user=request.user).delete()
            return JsonResponse({'success': True, 'message': 'Histórico limpo com sucesso'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)


# === VIEWS DE FEEDBACK ===

@login_required
def submit_feedback(request):
    """Submete feedback para uma resposta do chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            rating = data.get('rating')  # 'positive' ou 'negative'
            comment = data.get('comment', '')
            
            # Validações
            if not chat_id or rating not in ['positive', 'negative']:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Dados inválidos'
                }, status=400)
            
            # Verifica se o chat existe e pertence ao usuário
            try:
                chat = Chat.objects.get(id=chat_id, user=request.user)
            except Chat.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Chat não encontrado'
                }, status=404)
            
            # Metadados para analytics
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip_address = request.META.get('REMOTE_ADDR')
            
            # Atualiza ou cria feedback
            feedback, created = ChatFeedback.objects.update_or_create(
                chat=chat,
                user=request.user,
                defaults={
                    'rating': rating,
                    'comment': comment.strip()[:1000],  # Limite de 1000 caracteres
                    'user_agent': user_agent,
                    'ip_address': ip_address
                }
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Feedback enviado com sucesso',
                'feedback': {
                    'id': feedback.id,
                    'rating': feedback.rating,
                    'has_comment': bool(feedback.comment),
                    'created_at': feedback.created_at.isoformat(),
                    'is_new': created
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro interno: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


@login_required
def get_feedback_analytics(request):
    """Retorna analytics de feedback do usuário"""
    try:
        # Parâmetros opcionais
        days = int(request.GET.get('days', 30))
        
        # Calcula período
        from datetime import datetime, timedelta
        date_from = datetime.now() - timedelta(days=days)
        
        # Métricas gerais
        metrics = ChatFeedback.get_satisfaction_metrics(
            user=request.user,
            date_from=date_from
        )
        
        # Feedback recente
        recent_feedback = ChatFeedback.objects.filter(
            user=request.user,
            created_at__gte=date_from
        ).select_related('chat').order_by('-created_at')[:10]
        
        feedback_list = []
        for feedback in recent_feedback:
            feedback_list.append({
                'id': feedback.id,
                'rating': feedback.rating,
                'comment': feedback.comment,
                'created_at': feedback.created_at.isoformat(),
                'chat_message': feedback.chat.message[:100] + '...' if len(feedback.chat.message) > 100 else feedback.chat.message
            })
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'metrics': metrics,
                'recent_feedback': feedback_list,
                'period_days': days
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao buscar analytics: {str(e)}'
        }, status=500)


@login_required
def regenerate_response(request):
    """Regenera uma resposta do chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            
            if not chat_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'ID do chat é obrigatório'
                }, status=400)
            
            # Verifica se o chat existe e pertence ao usuário
            try:
                chat = Chat.objects.get(id=chat_id, user=request.user)
            except Chat.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Chat não encontrado'
                }, status=404)
            
            # Regenera a resposta
            message = chat.message
            llm_provider = data.get('llm_provider', 'databricks')
            
            try:
                # Busca semântica
                search_results = semantic_search(message)
                relevant_docs = filter_relevant_documents(search_results, message)
                
                # Gera nova resposta
                new_response = generate_answer(message, relevant_docs, llm_provider)
                
                # Atualiza a resposta no chat existente
                chat.response = new_response
                chat.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Resposta regenerada com sucesso',
                    'data': {
                        'chat_id': chat.id,
                        'response': new_response,
                        'response_html': markdown(new_response)
                    }
                })
                
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Erro ao regenerar resposta: {str(e)}'
                }, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'JSON inválido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro interno: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)


@login_required
def copy_response(request):
    """Registrar que uma resposta foi copiada (para analytics)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat_id = data.get('chat_id')
            
            # Verificar se o chat existe e pertence ao usuário
            chat = get_object_or_404(Chat, id=chat_id, user=request.user)
            
            # Log da ação (opcional - pode ser salvo em modelo específico)
            print(f"Resposta copiada - Chat ID: {chat_id}, User: {request.user.username}")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Ação registrada com sucesso'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos'
            }, status=400)
        except Exception as e:
            print(f"Erro ao registrar cópia: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Erro interno do servidor'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método não permitido'
    }, status=405)


@login_required
def chatbot_new(request, conversation_id=None):
    """View redirecionada para o novo template do chatbot"""
    return chatbot(request, conversation_id)


@login_required
def sobre(request):
    """View para a página Sobre o ChatCOTIN"""
    return render(request, 'sobre.html')
