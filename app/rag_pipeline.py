from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from .settings import EMBEDDING_MODEL, PERSIST_DIRECTORY, COLLECTION_NAME

class RAGPipeline:
    def __init__(self):
        self.llm = Ollama(model="llama3")
        self.embed_model = FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
        self.vectorstore = Chroma(
            embedding_function=self.embed_model,
            persist_directory=PERSIST_DIRECTORY,
            collection_name=COLLECTION_NAME
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={'k': 3})
        self.prompt_template = """Usa la siguiente información para responder a la pregunta del usuario.
Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.

Contexto: {context}
Pregunta: {question}

Solo devuelve la respuesta útil a continuación y nada más y responde siempre en español
Respuesta útil:
"""
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=['context', 'question']
        )
        self.qa_chain = self._setup_qa_chain()

    def _setup_qa_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def ask(self, query: str):
        response = self.qa_chain.invoke({"query": query})
        return response