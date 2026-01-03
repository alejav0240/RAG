from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import time

# Cargar variables de entorno
load_dotenv()

# 1. Configuración del LLM
# Nota: He usado gemini-1.5-flash que es la versión estable actual que soporta esta función
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY"), 
    temperature=0
)

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.7 , 
#     openai_api_key=os.getenv("OPENAI_API_KEY")
# )


# 2. Definición del Esquema de Salida (Pydantic)
# Esto define exactamente qué campos queremos recibir y de qué tipo son.
class SentimentResponse(BaseModel):
    sentimiento: str = Field(description="El sentimiento detectado: positivo, negativo o neutro")
    razon: str = Field(description="Una justificación breve del análisis de sentimiento")

# 3. Creación del LLM con Salida Estructurada
# Esta versión del LLM ya sabe que debe devolver un objeto 'SentimentResponse'
structured_llm = llm.with_structured_output(SentimentResponse)

def preprocess_text(text):
    """Limpia el texto eliminando espacios extras y limitando longitud"""
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
    """Genera un resumen conciso del texto"""
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    """Analiza el sentimiento usando el LLM estructurado"""
    prompt = f"Analiza el sentimiento del siguiente texto: {text}"
    
    try:
        # Invocamos el modelo estructurado. No necesitamos json.loads()
        # porque LangChain ya nos devuelve un objeto Pydantic validado.
        result = structured_llm.invoke(prompt)
        
        # Convertimos el objeto Pydantic a diccionario para que el resto
        # de tu cadena (merger) siga funcionando igual.
        return result.model_dump()
    except Exception as e:
        print(f"Error en análisis: {e}")
        return {"sentimiento": "neutro", "razon": "Error en validación de datos"}

sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    """Combina los resultados de ambas ramas en un formato unificado"""
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)

# Construcción de la cadena paralela
parallel_analyzer = RunnableParallel({
    "resumen": summary_branch, 
    "sentimiento_data": sentiment_branch
})

# Cadena principal
chain = preprocessor | parallel_analyzer | merger

# --- Pruebas ---
textos_prueba_batch = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

# Ejecutamos el ejemplo que te fallaba
resultados_batch = chain.batch(textos_prueba)

# Ejecutamos el ejemplo que te fallaba
# texto_especifico = textos_prueba[1]
# resultado = chain.invoke(texto_especifico)

print(resultados_batch)
