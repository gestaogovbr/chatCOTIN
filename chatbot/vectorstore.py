# Busca semântica otimizada para RAG
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_chroma import Chroma
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
CHROMA_COLLECTION = "meu_vetores"
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
