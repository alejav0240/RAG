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

loader = PyPDFDirectoryLoader("C:\\Proyectos\\RAG\\Temas\\Tema3\\contratos")
documents = loader.load()
mostrar_mensaje(f"Documentos Cargados {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

splitted_documents = splitter.split_documents(documents)
mostrar_mensaje(f"Documentos Splitted Total de Chunks {len(splitted_documents)}")

vectorstore = Chroma.from_documents(
    splitted_documents, 
    embedding=OpenAIEmbeddings(
        model="text-embedding-ada-002", 
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    persist_directory="C:\\Proyectos\\RAG\\Temas\\Tema3\\vectorstore"
)

mostrar_mensaje("Vectorstore Creado")

consulta = "¿Cual es el inmueble que forma parte del contrato en el que participa Maria Jimenez Campos?"

respuesta = vectorstore.similarity_search(consulta, k=3)
mostrar_mensaje("Respuesta Top 3 documentos similares ")
for i, doc in enumerate(respuesta):
    print(f"Contenido del documento {i+1}: {doc.page_content}")
    print(f"Metadata del documento {i+1}: {doc.metadata}")
    print("\n")

vectorstore.save_local("C:\\Proyectos\\RAG\\Temas\\Tema3\\vectorstore")
mostrar_mensaje("Vectorstore Guardado")
