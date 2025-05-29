from django.urls import path
from . import views


urlpatterns = [
    # URLs principais
    path('', views.chatbot, name='chatbot'),
    path('chatbot/', views.chatbot_new, name='chatbot_new'),
    path('sobre/', views.sobre, name='sobre'),
    path('conversation/<int:conversation_id>/', views.chatbot, name='chatbot_conversation'),
    
    # APIs da barra lateral
    path('api/conversations/', views.get_conversations_sidebar, name='get_conversations_sidebar'),
    path('api/conversations/search/', views.search_conversations, name='search_conversations'),
    path('api/conversations/new/', views.new_conversation, name='new_conversation'),
    path('api/conversations/<int:conversation_id>/load/', views.load_conversation, name='load_conversation'),
    path('api/conversations/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
    
    # APIs de feedback
    path('api/feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('api/feedback/analytics/', views.get_feedback_analytics, name='get_feedback_analytics'),
    path('api/response/regenerate/', views.regenerate_response, name='regenerate_response'),
    path('api/response/copy/', views.copy_response, name='copy_response'),
    
    # URLs existentes (compatibilidade)
    path('clear-history/', views.clear_history, name='clear_history'),
]
