from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import OllamaLLM as Ollama
from .settings import get_db_url

class SQLPipeline:
    def __init__(self):
        self.llm = Ollama(model="llama3")
        self._agents_cache = {}

    def _get_or_create_agent(self, db_name: str):
        if db_name in self._agents_cache:
            return self._agents_cache[db_name]

        db_url = get_db_url(db_name)
        if not db_url:
            raise ValueError(f"No se encontró la configuración para la base de datos: {db_name}")

        db = SQLDatabase.from_uri(db_url)
        
        print(f"Creando nuevo agente para la base de datos: {db_name}")
        
        agent_executor = create_sql_agent(
            llm=self.llm,
            db=db,
            verbose=True,
            max_iterations=7, 
            agent_executor_kwargs={"handle_parsing_errors": True}
        )
        
        self._agents_cache[db_name] = agent_executor
        return agent_executor

    def ask(self, query: str, db_name: str):
        try:
            agent = self._get_or_create_agent(db_name)
            
            # --- INICIO DEL PROMPT DE MÁXIMA PRECISIÓN ---
            prompt_template = f"""
            ### Rol y Objetivo:
            Eres un motor de API ultrapreciso que convierte preguntas de usuario en datos tabulares. Tu única función es devolver datos limpios.

            ### Instrucciones de Procesamiento:
            1.  Analiza la pregunta del usuario: `{query}`.
            2.  Genera y ejecuta la consulta SQL necesaria para obtener la respuesta.
            3.  Procesa el resultado de la consulta para la salida final.

            ### REGLAS ESTRICTAS DE FORMATO DE SALIDA:
            1.  **Formato de Tabla**: Si el resultado tiene filas y columnas, DEBES formatearlo como una tabla Markdown con la sintaxis correcta. La primera línea son los encabezados, la segunda es la línea separadora y las siguientes son los datos.
            
                **Ejemplo de sintaxis OBLIGATORIA:**
                ```markdown
                | Encabezado 1 | Encabezado 2 |
                | :--- | :--- |
                | dato fila 1 col 1 | dato fila 1 col 2 |
                | dato fila 2 col 1 | dato fila 2 col 2 |
                ```

            2.  **Formato de Celdas**: Si un valor en una celda es un valor compuesto como `(30, 4)`, DEBES limpiarlo. Elimina los paréntesis y muestra los números separados por coma y espacio, así: `30, 4`.

            3.  **Regla Absoluta de Salida**: Tu respuesta DEBE contener ÚNICAMENTE la tabla Markdown o la respuesta de texto simple. NO incluyas NINGUNA otra frase, explicación, nota, saludo o introducción. Tu respuesta final debe empezar directamente con el primer carácter de los datos (el `|` si es una tabla, o la primera letra si es un texto).

            ### Pregunta del Usuario:
            {query}
            """
            # --- FIN DEL PROMPT DE MÁXIMA PRECISIÓN ---
            
            response = agent.invoke({"input": prompt_template})
            return response.get("output", "No pude encontrar una respuesta.")
            
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return f"Lo siento, tuve un problema al consultar la base de datos '{db_name}'."