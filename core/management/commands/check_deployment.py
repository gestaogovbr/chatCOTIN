from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.core.management import call_command
import os
import sys

class Command(BaseCommand):
    help = 'Verifica se a aplicação está pronta para deploy no Azure'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Tenta corrigir problemas automaticamente',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Verificando configurações de deploy...\n')
        )
        
        issues = []
        warnings = []
        
        # 1. Verificar variáveis de ambiente críticas
        self.stdout.write('📋 Verificando variáveis de ambiente...')
        
        required_vars = [
            'SECRET_KEY',
            'DEBUG',
            'ALLOWED_HOSTS',
            'DATABRICKS_HOST',
            'DATABRICKS_TOKEN',
            'DATABRICKS_MODEL_ENDPOINT'
        ]
        
        for var in required_vars:
            value = getattr(settings, var, None)
            if not value or (isinstance(value, str) and not value.strip()):
                issues.append(f"❌ {var} não configurada")
            else:
                self.stdout.write(f"  ✅ {var}: OK")
        
        # 2. Verificar configurações de produção
        self.stdout.write('\n🔒 Verificando configurações de segurança...')
        
        if settings.DEBUG:
            issues.append("❌ DEBUG=True em produção (deve ser False)")
        else:
            self.stdout.write("  ✅ DEBUG: False")
        
        if settings.SECRET_KEY == 'django-insecure-zy)j@jjq%x@$&tzesq%87%wr0&^uwtr-!8c$1rmply839t*va7':
            issues.append("❌ SECRET_KEY padrão ainda em uso")
        else:
            self.stdout.write("  ✅ SECRET_KEY: Customizada")
        
        if 'localhost' in settings.ALLOWED_HOSTS and not settings.DEBUG:
            warnings.append("⚠️  localhost em ALLOWED_HOSTS (ok para testes)")
        
        # 3. Verificar banco de dados
        self.stdout.write('\n🗄️ Verificando banco de dados...')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write("  ✅ Conexão com banco: OK")
        except Exception as e:
            issues.append(f"❌ Erro de conexão com banco: {e}")
        
        # 4. Verificar arquivos essenciais
        self.stdout.write('\n📁 Verificando arquivos essenciais...')
        
        essential_files = [
            'requirements.txt',
            'manage.py',
            '.env.example',
            'startup.sh',
            'DEPLOY_AZURE.md'
        ]
        
        for file_path in essential_files:
            if os.path.exists(file_path):
                self.stdout.write(f"  ✅ {file_path}: Presente")
            else:
                issues.append(f"❌ {file_path}: Ausente")
        
        # 5. Verificar migrações
        self.stdout.write('\n🔄 Verificando migrações...')
        
        try:
            from django.db.migrations.executor import MigrationExecutor
            executor = MigrationExecutor(connection)
            pending_migrations = executor.migration_plan(executor.loader.graph.leaf_nodes())
            
            if pending_migrations:
                warnings.append(f"⚠️  {len(pending_migrations)} migrações pendentes")
            else:
                self.stdout.write("  ✅ Migrações: Todas aplicadas")
        except Exception as e:
            warnings.append(f"⚠️  Erro ao verificar migrações: {e}")
        
        # 6. Verificar arquivos estáticos
        self.stdout.write('\n📦 Verificando arquivos estáticos...')
        
        if options['fix']:
            try:
                call_command('collectstatic', '--noinput', verbosity=0)
                self.stdout.write("  ✅ Arquivos estáticos coletados")
            except Exception as e:
                issues.append(f"❌ Erro ao coletar estáticos: {e}")
        else:
            static_root = getattr(settings, 'STATIC_ROOT', None)
            if static_root and os.path.exists(static_root):
                self.stdout.write("  ✅ STATIC_ROOT configurado e presente")
            else:
                warnings.append("⚠️  Execute 'collectstatic' antes do deploy")
        
        # Resultado final
        self.stdout.write('\n' + '='*50)
        
        if issues:
            self.stdout.write(
                self.style.ERROR(f'\n❌ DEPLOY NÃO RECOMENDADO - {len(issues)} problemas críticos:')
            )
            for issue in issues:
                self.stdout.write(f"  {issue}")
            
            self.stdout.write(
                self.style.WARNING('\n💡 Corrija os problemas acima antes do deploy.')
            )
            sys.exit(1)
        
        elif warnings:
            self.stdout.write(
                self.style.WARNING(f'\n⚠️  DEPLOY COM ATENÇÃO - {len(warnings)} avisos:')
            )
            for warning in warnings:
                self.stdout.write(f"  {warning}")
            
            self.stdout.write(
                self.style.SUCCESS('\n✅ Aplicação pronta para deploy (com atenção aos avisos)')
            )
        
        else:
            self.stdout.write(
                self.style.SUCCESS('\n🚀 APLICAÇÃO PRONTA PARA DEPLOY!')
            )
            self.stdout.write(
                self.style.SUCCESS('Todas as verificações passaram com sucesso.')
            )
        
        # Instruções para DevOps
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS('\n📖 Para a equipe de DevOps:')
        )
        self.stdout.write('1. Consulte o arquivo DEPLOY_AZURE.md')
        self.stdout.write('2. Configure as variáveis do .env.example')
        self.stdout.write('3. Use o script startup.sh para inicialização')
        self.stdout.write('4. Configure health check em /health/')
        self.stdout.write('5. Monitore logs do Gunicorn e Django') 