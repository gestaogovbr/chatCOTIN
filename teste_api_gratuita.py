#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from chatbot.views import ask_rag_local
from chatbot.vectorstore import get_vectorstore

def test_api_gratuita():
    pergunta = "A API é gratuita?"
    print(f"Pergunta: {pergunta}")
    print("="*50)
    
    # Testar busca no vectorstore
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(pergunta, k=10)
    print("DOCUMENTOS ENCONTRADOS:")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. Fonte: {doc.metadata.get('filename', 'Desconhecida')}")
        print(f"Conteúdo: {doc.page_content[:300]}...")
        print("-"*30)
    
    print("\nRESPOSTA DO CHATCOTIN:")
    resposta = ask_rag_local(pergunta, k=5)
    print(resposta)

if __name__ == "__main__":
    test_api_gratuita() 