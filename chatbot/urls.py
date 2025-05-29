from django.urls import path
from . import views


urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('clear-history/', views.clear_history, name='clear_history'),
]
