from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps users with their tasks."),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}")
])

messages_history = [
    HumanMessage(content="Hello, how are you?"),
    AIMessage(content="I'm good, thanks! How about you?"),
    HumanMessage(content="I'm good too!"),
]

mensajes = chat_prompt.format_messages(
    messages=messages_history,
    question="What is the capital of France?"
)

for m in mensajes:
    print(m.content)