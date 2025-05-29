# Ingestão de documentos para RAG
import os
from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

SUPPORTED_EXTENSIONS = ['.txt', '.pdf', '.docx', '.csv', '.md']

DOCS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'DOCs')
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

def load_documents_from_folder(folder_path):
    """Carrega todos os documentos suportados de uma pasta."""
    docs = []
    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        file_path = os.path.join(folder_path, filename)
        if ext == '.txt' or ext == '.md':
            docs += TextLoader(file_path).load()
        elif ext == '.pdf':
            docs += UnstructuredPDFLoader(file_path).load()
        elif ext == '.docx':
            docs += UnstructuredWordDocumentLoader(file_path).load()
        elif ext == '.csv':
            docs += CSVLoader(file_path).load()
    return docs

def split_documents(documents, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

def ingest_documents(folder_path=DOCS_PATH, collection_name="meu_vetores", chunk_size=None, chunk_overlap=None):
    """Pipeline completo: carrega, divide, embute e indexa documentos no ChromaDB.
    chunk_size e chunk_overlap podem ser ajustados dinamicamente.
    """
    docs = load_documents_from_folder(folder_path)
    # Usa valores customizados se fornecidos, senão usa padrão
    cs = chunk_size if chunk_size is not None else 1000
    co = chunk_overlap if chunk_overlap is not None else 150
    chunks = split_documents(docs, chunk_size=cs, chunk_overlap=co)
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, collection_name=collection_name)
    return vectorstore
