from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import dotenv
import os

def mostrar_mensaje(mensaje):
    print("-"*50)
    print("_"*10 + f" {mensaje} " + "_"*10)
    print("-"*50)

dotenv.load_dotenv()

vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(
        model="text-embedding-ada-002", 
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    persist_directory="C:\\Proyectos\\RAG\\Temas\\Tema3\\vectorstore"
)

retriever = vectorstore.as_retriever(
    search_type="similarity", 
    search_kwargs={"k": 2}
)

mostrar_mensaje("Vectorstore Creado")

consulta = "¿Cual es el inmueble que forma parte del contrato en el que participa Maria Jimenez Campos?"

respuesta = retriever.invoke(consulta)
mostrar_mensaje("Respuesta Top 3 documentos similares ")
for i, doc in enumerate(respuesta):
    print(f"Contenido del documento {i+1}: {doc.page_content}")
    print(f"Metadata del documento {i+1}: {doc.metadata}")
    print("\n")

mostrar_mensaje("Vectorstore Guardado")
