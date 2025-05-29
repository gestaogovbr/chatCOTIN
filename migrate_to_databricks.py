#!/usr/bin/env python3
"""
Script de migração para Databricks Llama 4 Maverick
Este script ajuda a configurar o projeto para usar o Databricks em vez do Groq.
"""

import os
import sys
import subprocess

def check_env_file():
    """Verifica se o arquivo .env existe e tem as configurações necessárias"""
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado!")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = ['DATABRICKS_HOST', 'DATABRICKS_TOKEN', 'DATABRICKS_MODEL_ENDPOINT']
    missing_vars = []
    
    for var in required_vars:
        if var not in content or f'{var}=your-' in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente não configuradas: {', '.join(missing_vars)}")
        print("📝 Edite o arquivo .env e configure as variáveis necessárias.")
        return False
    
    print("✅ Arquivo .env configurado corretamente!")
    return True

def install_dependencies():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print(f"Saída do erro: {e.stderr}")
        return False

def test_databricks_connection():
    """Testa a conexão com o Databricks"""
    print("🔗 Testando conexão com Databricks...")
    
    try:
        # Importa as configurações do Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
        import django
        django.setup()
        
        from django.conf import settings
        from databricks_langchain import ChatDatabricks
        
        # Configura as variáveis de ambiente
        os.environ['DATABRICKS_HOST'] = settings.DATABRICKS_HOST
        os.environ['DATABRICKS_TOKEN'] = settings.DATABRICKS_TOKEN
        
        # Tenta criar o modelo
        model = ChatDatabricks(
            endpoint=settings.DATABRICKS_MODEL_ENDPOINT,
            temperature=0.7,
            max_tokens=100
        )
        
        # Testa uma mensagem simples
        response = model.invoke([("human", "Olá, você está funcionando?")])
        print("✅ Conexão com Databricks estabelecida com sucesso!")
        print(f"📝 Resposta de teste: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao conectar com Databricks: {e}")
        print("💡 Verifique suas credenciais e configurações no arquivo .env")
        return False

def main():
    """Função principal do script de migração"""
    print("🚀 Iniciando migração para Databricks Llama 4 Maverick")
    print("=" * 50)
    
    # Verifica o arquivo .env
    if not check_env_file():
        print("\n📋 Para configurar o .env, siga os passos:")
        print("1. Edite o arquivo .env na raiz do projeto")
        print("2. Configure DATABRICKS_HOST com a URL do seu workspace")
        print("3. Configure DATABRICKS_TOKEN com seu token de acesso")
        print("4. Configure DATABRICKS_MODEL_ENDPOINT com o nome do endpoint")
        print("\n📖 Consulte DATABRICKS_SETUP.md para instruções detalhadas")
        return False
    
    # Instala dependências
    if not install_dependencies():
        return False
    
    # Testa conexão
    if not test_databricks_connection():
        return False
    
    print("\n🎉 Migração concluída com sucesso!")
    print("🔧 Agora você pode executar: python manage.py runserver")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 