EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
PERSIST_DIRECTORY = "chroma_db_dir"
COLLECTION_NAME = "stanford_report_data"

# ---- Diccionario de Bases de Datos ----
# Agrega aquí todas las bases de datos que necesites.
# La clave (ej: "atlas_cmms") será el nombre que aparecerá en el menú.
DATABASES = {
    "atlas_cmms": {
        "user": "rootUser",
        "password": "mypassword",
        "host": "localhost",
        "port": "5432",
        "db_name": "atlas"
    },
}
# --- Función de ayuda para construir la URL de conexión ---
def get_db_url(db_name: str) -> str:
    db_info = DATABASES.get(db_name)
    if not db_info:
        return None
    return f"postgresql+psycopg2://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['db_name']}"