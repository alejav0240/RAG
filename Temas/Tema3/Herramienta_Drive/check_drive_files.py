from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle

# Rutas
base_path = "C:\\Proyectos\\RAG\\Temas\\Tema3\\Herramienta_Drive"
credentials_path = os.path.join(base_path, "credentials.json")
token_path = os.path.join(base_path, "token.json")
folder_id = "1v48BiGlixmjaIQFpbtDEEYgHKaJZKuFm"

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_credentials():
    """Obtiene las credenciales, renovándolas si es necesario."""
    creds = None
    
    # Si existe token.json, intentar cargarlo
    if os.path.exists(token_path):
        try:
            # Intentar cargar como pickle primero
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except:
            # Si falla, intentar como JSON
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                print(f"Error cargando token: {e}")
                creds = None
    
    # Si no hay credenciales válidas, obtener nuevas
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Renovando token expirado...")
            creds.refresh(Request())
        else:
            print("Iniciando flujo de autenticación OAuth...")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guardar las credenciales para la próxima ejecución
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print("Token guardado exitosamente")
    
    return creds

def list_files_in_folder(folder_id):
    """Lista todos los archivos en la carpeta de Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    print(f"\n{'='*60}")
    print(f"Buscando archivos en carpeta: {folder_id}")
    print(f"{'='*60}\n")
    
    try:
        # Buscar archivos en la carpeta
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, size, createdTime, modifiedTime)"
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print("⚠ No se encontraron archivos en la carpeta.")
            print("\nPor favor verifica:")
            print("1. Que la carpeta tenga archivos")
            print("2. Que el ID de la carpeta sea correcto")
            print("3. Que tienes permisos de acceso a la carpeta")
        else:
            print(f"✓ Se encontraron {len(files)} archivo(s):\n")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file['name']}")
                print(f"   - ID: {file['id']}")
                print(f"   - Tipo MIME: {file['mimeType']}")
                print(f"   - Tamaño: {file.get('size', 'N/A')} bytes")
                print(f"   - Modificado: {file.get('modifiedTime', 'N/A')}")
                print()
        
        return files
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        return []

if __name__ == "__main__":
    files = list_files_in_folder(folder_id)
