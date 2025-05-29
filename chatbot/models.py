from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import re


class Conversation(models.Model):
    """Modelo para agrupar chats em conversas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f'{self.user.username}: {self.title or "Nova Conversa"}'
    
    def generate_title(self):
        """Gera título automático baseado na primeira mensagem"""
        first_chat = self.chats.first()
        if first_chat and not self.title:
            # Extrai título da primeira mensagem (máximo 50 caracteres)
            title = first_chat.message[:50]
            # Remove caracteres especiais e quebras de linha
            title = re.sub(r'\s+', ' ', title).strip()
            if len(first_chat.message) > 50:
                title += "..."
            self.title = title
            self.save()
        return self.title
    
    def get_date_group(self):
        """Retorna grupo temporal para organização"""
        now = timezone.now()
        today = now.date()
        yesterday = (now - timedelta(days=1)).date()
        week_ago = (now - timedelta(days=7)).date()
        
        chat_date = self.updated_at.date()
        
        if chat_date == today:
            return 'today'
        elif chat_date == yesterday:
            return 'yesterday'
        elif chat_date >= week_ago:
            return 'this_week'
        else:
            return 'older'
    
    def get_messages_count(self):
        """Retorna número de mensagens na conversa"""
        return self.chats.count()


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='chats', null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username}: {self.message}'
    
    def save(self, *args, **kwargs):
        # Se não tem conversa, cria uma nova
        if not self.conversation and self.user:
            conversation = Conversation.objects.create(user=self.user)
            self.conversation = conversation
        
        super().save(*args, **kwargs)
        
        # Gera título automaticamente para a conversa
        if self.conversation:
            self.conversation.generate_title()
            # Atualiza timestamp da conversa
            self.conversation.updated_at = self.created_at
            self.conversation.save()
    
    def get_feedback_summary(self):
        """Retorna resumo do feedback desta resposta"""
        feedback = self.feedback.first()
        if feedback:
            return {
                'rating': feedback.rating,
                'has_comment': bool(feedback.comment),
                'created_at': feedback.created_at
            }
        return None


class ChatFeedback(models.Model):
    """Modelo para feedback das respostas do chatbot"""
    
    RATING_CHOICES = [
        ('positive', 'Útil'),
        ('negative', 'Não útil'),
    ]
    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True, help_text="Comentário opcional sobre o feedback")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metadados para analytics
    user_agent = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    session_duration = models.IntegerField(blank=True, null=True, help_text="Duração da sessão em segundos")
    
    class Meta:
        unique_together = ['chat', 'user']  # Um feedback por usuário por resposta
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.get_rating_display()} - Chat #{self.chat.id}'
    
    @classmethod
    def get_satisfaction_metrics(cls, user=None, date_from=None, date_to=None):
        """Calcula métricas de satisfação"""
        queryset = cls.objects.all()
        
        if user:
            queryset = queryset.filter(user=user)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        total = queryset.count()
        if total == 0:
            return {
                'total_feedback': 0,
                'positive_count': 0,
                'negative_count': 0,
                'satisfaction_rate': 0,
                'comments_count': 0
            }
        
        positive = queryset.filter(rating='positive').count()
        negative = queryset.filter(rating='negative').count()
        comments = queryset.exclude(comment__isnull=True).exclude(comment='').count()
        
        return {
            'total_feedback': total,
            'positive_count': positive,
            'negative_count': negative,
            'satisfaction_rate': round((positive / total) * 100, 2),
            'comments_count': comments
        }
