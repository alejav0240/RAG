# 📚 Proyecto RAG: Demostraciones Avanzadas con Langchain y LangGraph

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Langchain](https://img.shields.io/badge/Langchain-0.1.0%2B-green?style=for-the-badge&logo=langchain)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4%2B-purple?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjU2IiBoZWlnaHQ9IjI1NiIgdmlld0JveD0iMCAwIDI1NiAyNTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZmlsbD0iIzQxNDM0NSIgZD0iTTAgMGgyNTZ2MjU2SDBWMHoiLz48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTExOC40IDUyLjFoMTkuMnYxNTIuOGgtMTkuMnYtMTUyLjh6TTE1OS44IDkyLjNoMTkuMnYxMTIuOGgtMTkuMnYtMTEyLjh6TTc3IDExMi43aDE5LjJ2OTIuOGgtdDE5LjJ2LTkyLjh6TTM1LjQgMTMyLjRoMTkuMnY3Mi44aC0xOS4ydi03Mi44eiIvPjwvc3ZnPg==)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google)
![OpenAI GPT](https://img.shields.io/badge/OpenAI%20GPT-API-blueviolet?style=for-the-badge&logo=openai)

---

## 📝 Descripción del Proyecto

Este proyecto es una colección exhaustiva de ejemplos y demostraciones prácticas centradas en la implementación de patrones de Generación Aumentada por Recuperación (RAG) utilizando las potentes librerías `Langchain` y `LangGraph`. Desde la interacción básica con Modelos de Lenguaje (LLMs) hasta la construcción de sistemas complejos de recuperación de información y chatbots interactivos, este repositorio sirve como una guía y un recurso educativo invaluable para entender y aplicar estas tecnologías.

Explora cómo cargar documentos, dividir texto, generar embeddings, almacenar vectores, recuperar información relevante y construir aplicaciones de chat dinámicas.

---

## ✨ Características Principales

*   **Demostraciones RAG Completas:** 🧠 Cubre todo el ciclo de vida de un sistema RAG, incluyendo carga de documentos desde diversas fuentes (local, web, Google Drive), división eficiente de texto, generación de embeddings, almacenamiento vectorial (ChromaDB) y recuperación de información contextual.
*   **Ejemplos de Chatbots Interactivos:** 💬 Implementaciones de chatbots utilizando `Streamlit`, mostrando cómo construir interfaces de usuario conversacionales.
*   **Exploración de Prompt Engineering:** 💡 Ejemplos de plantillas de prompts, análisis de chat (sentimientos, parsing) para optimizar la interacción con los LLMs.
*   **Integración con Fuentes de Datos Externas:** 📂 Capacidad para cargar documentos desde Google Drive y otras fuentes web, ampliando la base de conocimiento del LLM.
*   **Soporte Multimodelo:** 🚀 Ejemplos de interacción con diferentes proveedores de LLMs, incluyendo Google Gemini y OpenAI (GPT), facilitando la experimentación y comparación.
*   **Estructura Modular y Educativa:** 📖 El proyecto está organizado temáticamente, lo que permite una comprensión paso a paso de cada componente de Langchain y LangGraph.

---

## 🛠️ Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

*   **Python 3.9+**
*   **`pip`** (gestor de paquetes de Python)

También necesitarás configurar tus claves API para los servicios de LLM que desees utilizar (Google Gemini, OpenAI GPT).

---

## 🚀 Instrucciones de Instalación

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/RAG.git # Reemplaza con la URL real de tu repositorio
    cd RAG
    ```

2.  **Crear un entorno virtual:**
    Se recomienda usar un entorno virtual para gestionar las dependencias del proyecto.

    ```bash
    python -m venv venv
    ```

3.  **Activar el entorno virtual:**

    *   **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **En Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Instalar las dependencias:**
    Asegúrate de tener un archivo `requirements.txt` en la raíz del proyecto con todas las dependencias listadas. Si no existe, deberás crearlo manualmente con las librerías mencionadas en la sección de tecnologías.

    ```bash
    pip install -r requirements.txt
    ```
    (Si no tienes un `requirements.txt`, puedes instalar las principales manualmente: `pip install langchain langgraph streamlit chromadb google-api-python-client openai google-generativeai pypdf tiktoken`)

5.  **Configurar las claves API:**
    Crea un archivo `.env` en la raíz del proyecto (o utiliza variables de entorno de tu sistema) y añade tus claves API:

    ```
    OPENAI_API_KEY="tu_clave_openai"
    GOOGLE_API_KEY="tu_clave_google_gemini"
    # Otras claves si son necesarias, por ejemplo, para Google Drive
    ```

---

## 🧑‍💻 Guía de Uso

El proyecto está estructurado para facilitar la exploración de cada componente. Aquí hay algunos ejemplos de cómo puedes utilizarlo:

1.  **Ejecutar un Chatbot con Streamlit:**
    Navega al directorio donde se encuentra el chatbot y ejecútalo.

    ```bash
    # Ejemplo:
    # cd Proyecto_RAG/Streamlit_Chatbot
    streamlit run streamlit_chatbot.py
    ```
    Esto abrirá una interfaz interactiva en tu navegador donde podrás chatear con el modelo.

2.  **Interactuar con Modelos de Lenguaje específicos:**
    Puedes ejecutar los scripts individuales para probar la interacción con diferentes LLMs.

    ```bash
    # Ejemplo con GPT:
    python Tema1/Hello_LLM/hello_gpt.py

    # Ejemplo con Gemini:
    python Tema1/Hello_LLM/hello_gemini.py
    ```

3.  **Cargar y procesar documentos:**
    Explora los scripts en los directorios de carga de documentos para entender cómo se ingieren y procesan los datos.

    ```bash
    # Ejemplo de carga de documentos local:
    python Tema2/Document_Loaders/document_loadres.py
    ```

4.  **Experimentar con RAG:**
    Los directorios `Vector_Storage`, `Embedding` y `Retrivers` contienen ejemplos clave para entender el flujo RAG.

    ```bash
    # Ejemplo de generación de embeddings:
    python Tema2/Embedding/embedding_langchain.py
    ```

---

## 🏗️ Estructura del Proyecto

El proyecto está organizado de manera modular por "Temas" y "Proyectos" para una fácil navegación y comprensión de los diferentes conceptos y funcionalidades.

```bash
RAG/
├── Tema1/
│   ├── Hello_LLM/
│   │   ├── hello_gpt.py          # Interacción básica con OpenAI GPT
│   │   └── hello_gemini.py       # Interacción básica con Google Gemini
│   └── Prompt_Engineering/
│       ├── promt_template.py     # Ejemplos de plantillas de prompts
│       ├── rol_prompt_template.py# Plantillas de prompts con roles
│       ├── chat_parse.py         # Análisis y parsing de chat
│       └── chat_sentimientos.py  # Análisis de sentimientos en el chat
├── Tema2/
│   ├── Document_Loaders/
│   │   ├── document_loadres.py   # Carga de documentos locales (PDFs, etc.)
│   │   └── webBase_loaders.py    # Carga de documentos desde la web
│   ├── Text_Spliters/
│   │   └── text_spliters.py      # Estrategias para dividir texto
│   ├── Embedding/
│   │   └── embedding_langchain.py# Generación de embeddings con Langchain
│   ├── Vector_Storage/
│   │   └── vector_storage.py     # Almacenamiento de vectores (ChromaDB)
│   │   └── vectorstore/          # Directorio para la base de datos vectorial
│   │       └── chroma.sqlite3    # Base de datos ChromaDB
│   └── Retrivers/
│       └── retrivers_langchain.py# Recuperación de información
├── Tema3/
│   ├── Herramienta_Drive/
│   │   ├── google_loader.py      # Carga de documentos desde Google Drive
│   │   ├── credentials.json      # Credenciales para Google Drive API
│   │   └── token.json            # Token de autenticación de Google Drive API
│   └── Agentes/
│       └── ...                   # Ejemplos de agentes
├── Proyecto_RAG/
│   ├── streamlit_chatbot.py      # Aplicación de chatbot con Streamlit
│   └── ...                       # Otros componentes del proyecto RAG
├── contratos/                    # Directorio de ejemplo con documentos PDF
│   └── contrato_ejemplo.pdf
└── requirements.txt              # Dependencias del proyecto
```

---

## 💻 Tecnologías Utilizadas

*   **Lenguaje de Programación:** Python
*   **Frameworks de LLM:**
    *   [Langchain](https://www.langchain.com/)
    *   [LangGraph](https://langchain-ai.github.io/langgraph/)
*   **Bases de Datos Vectoriales:**
    *   [ChromaDB](https://www.trychroma.com/)
*   **Frameworks Web/UI:**
    *   [Streamlit](https://streamlit.io/)
*   **Integraciones y APIs:**
    *   Google Drive API
    *   OpenAI API (GPT models)
    *   Google Gemini API
*   **Librerías de Procesamiento de Documentos:**
    *   `pypdf` (o similar)
    *   `tiktoken`

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este proyecto, añadir nuevas demostraciones o corregir errores, por favor, abre un "issue" o envía un "pull request".

1.  Haz un "fork" del repositorio.
2.  Crea una nueva rama (`git checkout -b feature/nueva-demostracion`).
3.  Realiza tus cambios y haz "commit" (`git commit -m 'feat: añade nueva demostración X'`).
4.  Empuja tus cambios a tu "fork" (`git push origin feature/nueva-demostracion`).
5.  Abre un "pull request" explicando tus cambios.