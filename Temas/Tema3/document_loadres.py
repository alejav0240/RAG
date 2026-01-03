from langchain_community.document_loaders import PyPDFLoader

path = 'C:/Users/aleja/Downloads/Alejandro-Chipana-Backend-Developer-Intermedio.pdf'

loader = PyPDFLoader(path)

pages = loader.load()

for i, page in enumerate(pages):
    print(f"Pagina: {i}")
    print("Contenido: ",page.page_content)
    print("Metadata: ",page.metadata)
    