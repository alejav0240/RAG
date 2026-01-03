from langchain_community.document_loaders import WebBaseLoader

url = 'https://boda-erik.vercel.app/'

loader = WebBaseLoader(url)

docs = loader.load()

for i, page in enumerate(pages):
    print(f"Pagina: {i}")
    print("Contenido: ",page.page_content)
    print("Metadata: ",page.metadata)
    