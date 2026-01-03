from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAIfrom 
from models.cv_models import AnalisisCV
from prompts.cv_prompts import crear_sistema_prompts
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def crear_evaluador_cv():
    modelo_base = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )
    modelo_estrucutrado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    
    cadena_evaluacion = chat_prompt | modelo_estrucutrado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str):
    try:
        evaluador = crear_evaluador_cv()
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        resultado = evaluador.invoke({
            "texto_cv": texto_cv, 
            "descripcion_puesto": descripcion_puesto,
            "fecha_actual": fecha_hoy
        })
        return resultado
    except Exception as e:
        print(f"Error al evaluar el candidato: {str(e)}")
        return AnalisisCV(
            nombre_candidato="Error al evaluar el candidato",
            experiencia_laboral=0,
            habilidades_clave=["Error al evaluar el candidato"],
            educacion="Error no se pudo evaluar la educacion",
            experiencia_relevante="Error al evaluar la experiencia relevante",
            fortalezas=["Requiere revision manual"],
            areas_mejora=["Verifique el CV"],
            porcentaje_ajuste=0
        )
    