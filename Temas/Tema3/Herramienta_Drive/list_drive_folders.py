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

def list_my_drive_items():
    """Lista las carpetas y archivos recientes en Mi unidad."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    print(f"\n{'='*80}")
    print("CARPETAS EN MI UNIDAD DE GOOGLE DRIVE")
    print(f"{'='*80}\n")
    
    try:
        # Listar carpetas
        query = "mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=20,
            fields="files(id, name, parents, createdTime)",
            orderBy="modifiedTime desc"
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            print(f"✓ Carpetas encontradas ({len(folders)}):\n")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder['name']}")
                print(f"   - ID: {folder['id']}")
                print(f"   - Creada: {folder.get('createdTime', 'N/A')}")
                print()
        
        print(f"\n{'='*80}")
        print("ARCHIVOS RECIENTES (PDF y DOCS)")
        print(f"{'='*80}\n")
        
        # Listar PDFs y documentos
        query = "(mimeType='application/pdf' or mimeType='application/vnd.google-apps.document' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document') and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=20,
            fields="files(id, name, mimeType, parents, modifiedTime)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            print(f"✓ Archivos encontrados ({len(files)}):\n")
            for i, file in enumerate(files, 1):
                print(f"{i}. {file['name']}")
                print(f"   - ID: {file['id']}")
                print(f"   - Tipo: {file['mimeType']}")
                print(f"   - Padres: {file.get('parents', ['root'])}")
                print(f"   - Modificado: {file.get('modifiedTime', 'N/A')}")
                print()
        else:
            print("⚠ No se encontraron archivos PDF o documentos recientes")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    list_my_drive_items()
