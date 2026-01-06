# Use the advanced version.
from langchain_googledrive.document_loaders import GoogleDriveLoader
import os
import tempfile

# Rutas absolutas para evitar errores de "archivo no encontrado"
base_path = "C:\\Proyectos\\RAG\\Temas\\Tema3\\Herramienta_Drive"
credentials_path = os.path.join(base_path, "credentials.json")
token_path = os.path.join(base_path, "token.json")
folder_id = "1v48BiGlixmjaIQFpbtDEEYgHKaJZKuFm"

SCOPES = ["https://www.googleapis.com/auth/drive.readonly","https://www.googleapis.com/auth/drive.file"]

print(f"\n{'='*60}")
print("Iniciando carga de documentos desde Google Drive")
print(f"{'='*60}")
print(f"Carpeta ID: {folder_id}")
print(f"Credentials: {credentials_path}")
print(f"Token: {token_path}")

# Es vital que el archivo credentials.json exista en esa ruta exacta
if not os.path.exists(credentials_path):
    print(f"ERROR: No se encuentra el archivo en {credentials_path}")
else:
    print(f"✓ Archivo credentials.json encontrado")
    
    if os.path.exists(token_path):
        print(f"✓ Token existente encontrado")
    else:
        print(f"⚠ No existe token.json - Se iniciará autenticación OAuth")
    
    try:
        # Opción 1: Sin especificar file_types para cargar todos los archivos
        print(f"\n{'='*60}")
        print("Configurando loader...")
        print(f"{'='*60}")
        
        loader = GoogleDriveLoader(
            folder_id=folder_id,
            credentials_path=credentials_path,
            token_path=token_path,
            recursive=False,  # No recursivo para evitar problemas
            scopes=SCOPES,
            # No especificamos file_types para que intente cargar todos
        )

        print(f"\n{'='*60}")
        print("Cargando documentos...")
        print(f"{'='*60}")
        
        # Intentar cargar documentos
        try:
            documents = loader.load()
            
            print(f"\n{'='*60}")
            print(f"✓ Se cargaron {len(documents)} documentos.")
            print(f"{'='*60}\n")
            
            if len(documents) > 0:
                for i, doc in enumerate(documents, 1):
                    print(f"{i}. Documento:")
                    print(f"   - Origen: {doc.metadata.get('source', 'N/A')}")
                    print(f"   - Título: {doc.metadata.get('title', 'N/A')}")
                    
                    # Mostrar todos los metadatos disponibles
                    print(f"   - Metadatos disponibles: {list(doc.metadata.keys())}")
                    
                    # Mostrar tamaño del contenido
                    content_length = len(doc.page_content)
                    print(f"   - Tamaño contenido: {content_length} caracteres")
                    
                    # Mostrar preview del contenido (primeros 200 caracteres)
                    if content_length > 0:
                        preview = doc.page_content[:200].replace('\n', ' ')
                        print(f"   - Preview: {preview}...")
                    else:
                        print(f"   - Contenido vacío")
                    print()
            else:
                print("\n⚠ ADVERTENCIA: No se encontraron documentos en la carpeta.")
                
        except UnicodeDecodeError as e:
            print(f"\n⚠ ERROR de codificación: {str(e)}")
            print("Intentando con configuración alternativa...")
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        print("\nDetalles del error:")
        traceback.print_exc()
