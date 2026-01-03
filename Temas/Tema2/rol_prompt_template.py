from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

plantilla_sistema = SystemMessagePromptTemplate.from_template("" \
    "Eres un {rol} especializado en {especialidad}. " \
    "Respponde de manera {tono}."\
    "Tu objetivo es ayudar al usuario a resolver su problema. " \
    "Si no tienes la respuesta, di que no la tienes y proporciones una alternativa. " \
    "Si no entiendes la pregunta, pide clarificación al usuario. " \
    "Si el usuario pide algo fuera de tu especialidad, di que no puedes ayudar y proporciones una alternativa."
)

plantilla_usuario = HumanMessagePromptTemplate.from_template(
    "Mi preguna es sobre {tema} es: {pregunta}"
)

plantilla_chat = ChatPromptTemplate.from_messages([
    plantilla_sistema,
    plantilla_usuario
])

mensajes = plantilla_chat.format_messages(
    rol="C# developer",
    especialidad="desarrollo de software con .net core",
    tono="formal",
    tema="patrones de diseño",
    pregunta="¿Cual es el patron de diseño singleton?"
)

for mensaje in mensajes:
    print(mensaje.content)