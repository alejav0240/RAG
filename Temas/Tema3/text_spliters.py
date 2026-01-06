from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
import dotenv
import os

dotenv.load_dotenv()

PDF_PATH = "C:\Proyectos\RAG\Temas\Tema3\Herramienta_Drive\Alejandro-Chipana-Backend-Developer-Intermedio.pdf"

loader = PyPDFLoader(PDF_PATH)
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)

chunks = text_splitter.split_documents(pages)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.2
)

sumaries = []

for chunk in chunks:
    print(chunk.page_content)
    response = llm.invoke(chunk.page_content)
    sumaries.append(response.content)

final_summary = llm.invoke("Combinar los siguientes resumen en un solo documento:\n\n" + "\n\n".join(sumaries))
print(final_summary.content)