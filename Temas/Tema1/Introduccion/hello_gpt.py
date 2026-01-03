import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini",temperature=0.7 , openai_api_key=os.getenv("OPENAI_API_KEY"))

pregunta = 'Hola, como estas?'
print('Pregunta: ',pregunta)

response = llm.invoke(pregunta)
print('Respuesta: ',response.content)