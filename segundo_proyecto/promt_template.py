from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that helps users with their tasks."),
    ("human", "{text}")
])

message = chat_prompt.format_messages(text="Hello, how are you?")
print(message)