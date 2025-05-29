# Busca semântica otimizada para RAG
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Atualizado para usar a coleção mais recente com todos os documentos
CHROMA_COLLECTION = "chatcotin_knowledge_1748485543"
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")


def get_vectorstore(collection_name=CHROMA_COLLECTION, persist_directory=CHROMA_PERSIST_DIR):
    """Carrega o vectorstore ChromaDB já indexado."""
    embeddings = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_directory
    )


def semantic_search(query, k=5, collection_name=CHROMA_COLLECTION):
    """Busca semântica otimizada: retorna os k documentos mais relevantes para a query."""
    vectorstore = get_vectorstore(collection_name=collection_name)
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


def enhanced_search_for_panels(query, k=8):
    """
    Busca especializada para consultas sobre painéis que garante a inclusão 
    do chunk do markdown com a lista completa de painéis.
    """
    vectorstore = get_vectorstore()
    
    # Busca normal
    normal_results = vectorstore.similarity_search(query, k=k)
    
    # Verificar se algum resultado já inclui o chunk do markdown
    markdown_chunk_found = False
    for result in normal_results:
        if ('resumo_fontes_transparencia_ativa.md' in result.metadata.get('filename', '') and
            'Painel de Compras Governamentais' in result.page_content and
            'Portal Nacional de Contratações Públicas' in result.page_content):
            markdown_chunk_found = True
            break
    
    # Se não encontrou o chunk do markdown, forçar sua inclusão
    if not markdown_chunk_found:
        # Buscar especificamente o chunk do markdown
        markdown_results = vectorstore.similarity_search(
            "Painel de Compras Governamentais Portal Nacional de Contratações Públicas PNCP", 
            k=10
        )
        
        # Encontrar o chunk correto do markdown
        for result in markdown_results:
            if ('resumo_fontes_transparencia_ativa.md' in result.metadata.get('filename', '') and
                'Painel de Compras Governamentais' in result.page_content):
                # Substituir o último resultado pela informação do markdown
                normal_results[-1] = result
                print("🔧 Chunk do markdown forçadamente incluído no contexto")
                break
    
    return [doc.page_content for doc in normal_results]


def is_panel_related_query(query):
    """Verifica se a consulta é relacionada a painéis."""
    query_lower = query.lower()
    panel_keywords = [
        'painéis', 'painel', 'panel', 'paineis', 
        'disponíveis', 'transparência', 'dashboards',
        'compras governamentais', 'pncp', 'município',
        'fornecedores', 'contratos públicos'
    ]
    return any(keyword in query_lower for keyword in panel_keywords)


# Palavras-chave do domínio (pode ser expandido/configurado)
DOMAIN_KEYWORDS = [
    "transparência", "dados abertos", "licitação", "compras", "governo", "LAI", "normativo", "portal", "sistema", "acesso", "informação", "lei", "decreto"
]


def filter_relevant_documents(question, documents, embeddings, threshold=0.3, top_n=5):
    """
    Filtra documentos relevantes combinando similaridade, palavras-chave e matching de termos da pergunta.
    """
    if not documents:
        return []
    try:
        question_embedding = np.array(embeddings.embed_query(question)).reshape(1, -1)
        doc_embeddings = np.array([
            np.array(embeddings.embed_query(doc.page_content))
            for doc in documents
        ])
        similarities = cosine_similarity(question_embedding, doc_embeddings)[0]
        question_lower = question.lower()
        filtered_docs = []
        for doc, sim in zip(documents, similarities):
            doc_lower = doc.page_content.lower()
            keyword_score = sum(1 for kw in DOMAIN_KEYWORDS if kw in doc_lower)
            question_words = question_lower.split()
            word_match_score = sum(1 for word in question_words if len(word) > 3 and word in doc_lower)
            final_score = sim + (keyword_score * 0.05) + (word_match_score * 0.1)
            if final_score >= threshold:
                filtered_docs.append((doc, final_score))
        filtered_docs = sorted(filtered_docs, key=lambda x: x[1], reverse=True)
        relevant_docs = [doc for doc, _ in filtered_docs[:top_n]]
        # Fallback: se não encontrou suficientes, retorna os top-N por similaridade
        if not relevant_docs:
            top_docs = sorted(zip(documents, similarities), key=lambda x: x[1], reverse=True)
            relevant_docs = [doc for doc, _ in top_docs[:top_n]]
        return relevant_docs
    except Exception as e:
        print(f"[Filtro de relevância] Erro: {e}")
        return documents[:top_n]
