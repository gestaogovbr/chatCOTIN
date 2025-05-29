from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint para Azure App Service
    Retorna status da aplicação para monitoramento
    """
    try:
        # Verificações básicas
        status = {
            'status': 'healthy',
            'django': True,
            'database': False,
            'databricks': False,
            'version': '1.0.0'
        }
        
        # Teste de conexão com database
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                status['database'] = True
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")
            status['database'] = False
        
        # Teste básico do Databricks (sem fazer chamada real)
        try:
            databricks_host = getattr(settings, 'DATABRICKS_HOST', '')
            databricks_token = getattr(settings, 'DATABRICKS_TOKEN', '')
            if databricks_host and databricks_token:
                status['databricks'] = True
            else:
                status['databricks'] = False
                status['databricks_config'] = 'missing_credentials'
        except Exception as e:
            logger.warning(f"Databricks config check failed: {e}")
            status['databricks'] = False
        
        # Determinar status geral
        if status['database'] and status['databricks']:
            status['status'] = 'healthy'
            return JsonResponse(status, status=200)
        else:
            status['status'] = 'degraded'
            return JsonResponse(status, status=200)  # Ainda 200 mas degraded
            
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def status(request):
    """
    Status endpoint mais detalhado para debug
    """
    try:
        return JsonResponse({
            'application': 'Chatbot Django Databricks',
            'version': '1.0.0',
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
            'databricks_configured': bool(getattr(settings, 'DATABRICKS_HOST', '')),
            'database_engine': settings.DATABASES['default']['ENGINE'],
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500) 