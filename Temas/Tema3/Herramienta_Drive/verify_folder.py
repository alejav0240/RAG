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
    
    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except:
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except:
                creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_folder_info(folder_id):
    """Obtiene información detallada de una carpeta específica."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    print(f"\n{'='*80}")
    print("VERIFICACIÓN DE CARPETA")
    print(f"{'='*80}\n")
    print(f"ID de carpeta: {folder_id}\n")
    
    try:
        # Intentar obtener información de la carpeta
        folder = service.files().get(
            fileId=folder_id,
            fields="id, name, mimeType, owners, shared, capabilities"
        ).execute()
        
        print("✓ Carpeta encontrada:")
        print(f"  - Nombre: {folder['name']}")
        print(f"  - Tipo MIME: {folder['mimeType']}")
        print(f"  - Compartida: {folder.get('shared', 'N/A')}")
        print(f"  - Propietarios: {[owner.get('emailAddress', 'N/A') for owner in folder.get('owners', [])]}")
        print(f"  - Puede listar: {folder.get('capabilities', {}).get('canListChildren', 'N/A')}")
        print()
        
        # Listar archivos en la carpeta
        print(f"{'='*80}")
        print("ARCHIVOS EN LA CARPETA")
        print(f"{'='*80}\n")
        
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, size, modifiedTime, exportLinks)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print("⚠ La carpeta está vacía o no contiene archivos visibles")
        else:
            print(f"✓ Se encontraron {len(files)} archivo(s):\n")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file['name']}")
                print(f"   - ID: {file['id']}")
                print(f"   - Tipo MIME: {file['mimeType']}")
                
                # Mostrar información específica para Google Docs
                if 'google-apps' in file['mimeType']:
                    print(f"   - Es un documento de Google")
                    if 'exportLinks' in file:
                        print(f"   - Puede exportarse a: {list(file['exportLinks'].keys())}")
                else:
                    print(f"   - Tamaño: {file.get('size', 'N/A')} bytes")
                
                print(f"   - Modificado: {file.get('modifiedTime', 'N/A')}")
                print()
        
        return files
        
    except Exception as e:
        print(f"❌ ERROR al acceder a la carpeta:")
        print(f"   {str(e)}")
        print(f"\nPosibles causas:")
        print("  1. El ID de la carpeta es incorrecto")
        print("  2. No tienes permisos para acceder a esta carpeta")
        print("  3. La carpeta fue eliminada")
        print(f"\nVerifica que el ID de la carpeta sea correcto")
        print(f"El ID debe verse así en la URL de Google Drive:")
        print(f"https://drive.google.com/drive/folders/[ID_DE_LA_CARPETA]")
        return []

if __name__ == "__main__":
    files = get_folder_info(folder_id)
