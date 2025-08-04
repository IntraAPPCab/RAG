from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Importa las clases de los pipelines y las configuraciones
from .rag_pipeline import RAGPipeline
from .sql_pipeline import SQLPipeline
from .settings import DATABASES

# Inicializa la aplicación FastAPI
app = FastAPI()

# Crea una instancia de cada pipeline
rag_pipeline = RAGPipeline()
sql_pipeline = SQLPipeline()

# Configura el directorio de plantillas HTML
templates = Jinja2Templates(directory="app/templates")

# Configura el directorio de archivos estáticos (para el favicon, etc.)
app.mount("/static", StaticFiles(directory="app/templates"), name="static")

# Define el modelo de datos para las preguntas que llegan a la API
class Query(BaseModel):
    question: str
    source: str

# Endpoint principal para servir la página del chat
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    # Obtiene los nombres de las bases de datos desde el archivo de configuración
    db_names = list(DATABASES.keys())
    # Renderiza el HTML y le pasa la lista de nombres de bases de datos
    return templates.TemplateResponse("chat.html", {"request": request, "db_names": db_names})

# Endpoint para recibir las preguntas y devolver respuestas
@app.post("/ask")
def ask_question(query: Query):
    try:
        source = query.source
        
        # Si la fuente es "documents", usa el pipeline de RAG
        if source == "documents":
            print("Query a los documentos...")
            response = rag_pipeline.ask(query.question)
            return {
                "result": response['result'],
                "source_documents": [
                    {"page": doc.metadata.get('page'), "file_path": doc.metadata.get('file_path')}
                    for doc in response['source_documents']
                ]
            }
        
        # Si la fuente es una de las bases de datos configuradas, usa el pipeline de SQL
        elif source in DATABASES:
            print(f"Query a la base de datos: {source}...")
            result = sql_pipeline.ask(query.question, db_name=source)
            return {"result": result, "source_documents": []}
            
        # Si la fuente no es válida, devuelve un error
        else:
            raise HTTPException(status_code=400, detail=f"Fuente de datos no válida: {source}")

    except Exception as e:
        # Manejo de errores generales
        raise HTTPException(status_code=500, detail=str(e))