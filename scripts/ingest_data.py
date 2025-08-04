import os
import glob
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from app.settings import EMBEDDING_MODEL, PERSIST_DIRECTORY, COLLECTION_NAME

def ingest_multiple_pdfs(pdfs_directory: str):
    # Paso 1: Buscar todos los archivos PDF en el directorio especificado.
    pdf_files = glob.glob(os.path.join(pdfs_directory, "*.pdf"))
    
    if not pdf_files:
        print(f"No se encontraron archivos PDF en la carpeta '{pdfs_directory}'.")
        return

    print(f"Encontrados {len(pdf_files)} archivos PDF para procesar.")
    
    all_docs = []
    # Paso 2: Procesar cada PDF en un bucle.
    for pdf_path in pdf_files:
        print(f"Procesando: {os.path.basename(pdf_path)}")
        loader = PyMuPDFLoader(pdf_path)
        data_pdf = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        docs = text_splitter.split_documents(data_pdf)
        all_docs.extend(docs)

    if not all_docs:
        print("No se pudo extraer contenido de los archivos PDF.")
        return

    # Paso 3: Crear los embeddings y guardar todos los documentos en ChromaDB de una sola vez.
    print(f"\nCreando embeddings para {len(all_docs)} fragmentos de documentos...")
    embed_model = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
    
    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
    
    _ = Chroma.from_documents(
        documents=all_docs,
        embedding=embed_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )
    print("¡Todos los documentos han sido cargados exitosamente! ✅")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_directory = os.path.join(project_root, 'source')
    
    ingest_multiple_pdfs(source_directory)