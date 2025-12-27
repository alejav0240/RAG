from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages  import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

# Configuración de LangChain
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-exp", "gemini-2.0-flash-2024-06-01"])
    
    # ¿Cómo recrearías el modelo con los nuevos parámetros?
    llm = ChatGoogleGenerativeAI(model=model_name,temperature=temperature , google_api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración de Streamlit
st.set_page_config(page_title="Chatbot con LangChain", page_icon=":robot_face:")
st.title("Chatbot Basico con LangChain")
st.markdown("Este es un chat bot de ejemplo con streamlit y langchain")

if st.button("🗑️ Nueva conversación"):
    # ¿Qué necesitas limpiar?
    # ¿Qué función de Streamlit refresca la página?
    st.session_state.messages = []
    st.rerun()


# Crear un chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Crear un prompt
prompt_template = PromptTemplate(
input_variables=["mensaje", "historial"],
template="""Eres un asistente útil y amigable llamado ChatBot Pro. 
Historial de conversación:
{historial}

Responde de manera clara y concisa a la siguiente pregunta: {mensaje}"""
)

chain = prompt_template | llm    


# Mostrar el chat history
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    
# Capturar la entrada del usuario
pregunta = st.chat_input("¿En qué puedo ayudarte?")

if pregunta:
    # mostrar la pregunta del usuario
    with st.chat_message("human"):
        st.markdown(pregunta)
    # Generar la respuesta
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Magia de streaming 
            for chunk in chain.stream({"mensaje": pregunta, "historial": st.session_state.messages}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante

            response_placeholder.markdown(full_response)

        # Almacenar los mensajes
        st.session_state.messages.append(HumanMessage(content=pregunta))
        st.session_state.messages.append(AIMessage(content=full_response))
    except Exception as e:
        # ¿Qué tipo de errores podrían ocurrir aquí?
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")