from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
    path('', include('accounts.urls')),
    
    # Health check endpoints para Azure
    path('health/', views.health_check, name='health_check'),
    path('status/', views.status, name='status'),
]
