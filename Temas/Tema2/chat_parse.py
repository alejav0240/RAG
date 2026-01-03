from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()

class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto")
    sentimientos: str = Field(description="Sentimientos del texto (Positivo, Negativo, Neutral)")
    
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.5)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_de_ejemplo = "No me encanto la comida en el restaurante, estaba muy mal hecha"

resultado = structured_llm.invoke(f"Analiza el siguiente texto: {texto_de_ejemplo}")

print(resultado)