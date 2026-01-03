import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI   
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.7 , google_api_key=os.getenv("GOOGLE_API_KEY"))


'''Plantillas avanzadas''' 
plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre: {nombre}\nAsistente: "
)

# --- Chain con LCEL (usando el operador pipe |) ---
# Esto reemplaza a LLMChain y es el nuevo estándar.
chain = plantilla | llm 

# --- Usando el chain ---
# Se usa .invoke() para cadenas en LCEL
resultado = chain.invoke({"nombre": "Juan"})

# La salida es un objeto 'AIMessage', su contenido de texto se accede con .content
print(resultado.content)
