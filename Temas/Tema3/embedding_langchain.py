from langchain_openai import OpenAIEmbeddings
import numpy as np
import dotenv
import os

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))

texto1 = "La Capital de Francia es Paris."
texto2 = "Paris es la ciudad capital de Francia."
texto3 = "La capital de Alemania es Berlín."
texto4 = "Berlín es la capital de Alemania."

vec1 = embeddings.embed_query(texto1)
vec2 = embeddings.embed_query(texto2)
vec3 = embeddings.embed_query(texto3)
vec4 = embeddings.embed_query(texto4)

print(f"Dimension del vector: {len(vec1)}")

print(f"Similaridad entre vec1 y vec2: {np.dot(vec1, vec2)}")
print(f"Similaridad entre vec1 y vec3: {np.dot(vec1, vec3)}")
print(f"Similaridad entre vec1 y vec4: {np.dot(vec1, vec4)}")

cos_sim_1_2 = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
cos_sim_1_3 = np.dot(vec1, vec3) / (np.linalg.norm(vec1) * np.linalg.norm(vec3))
cos_sim_1_4 = np.dot(vec1, vec4) / (np.linalg.norm(vec1) * np.linalg.norm(vec4))

print(f"Similaridad coseno entre vec1 y vec2: {cos_sim_1_2}")
print(f"Similaridad coseno entre vec1 y vec3: {cos_sim_1_3}")
print(f"Similaridad coseno entre vec1 y vec4: {cos_sim_1_4}")
