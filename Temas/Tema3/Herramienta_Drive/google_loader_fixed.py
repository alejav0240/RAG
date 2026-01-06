from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import pickle
import io
from PyPDF2 import PdfReader

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

def download_and_process_files(folder_id):
    """Descarga y procesa archivos de Google Drive."""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    print(f"\n{'='*80}")
    print("CARGANDO DOCUMENTOS DESDE GOOGLE DRIVE")
    print(f"{'='*80}\n")
    print(f"Carpeta ID: {folder_id}\n")
    
    try:
        # Buscar archivos en la carpeta
        query = f"'{folder_id}' in parents and trashed=false"
        results = service.files().list(
            q=query,
            pageSize=100,
            fields="files(id, name, mimeType, size, exportLinks)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print("⚠ No se encontraron archivos en la carpeta.")
            return []
        
        print(f"✓ Se encontraron {len(files)} archivo(s)\n")
        documents = []
        
        for i, file in enumerate(files, 1):
            print(f"{i}. Procesando: {file['name']}")
            print(f"   - Tipo MIME: {file['mimeType']}")
            
            content = ""
            
            try:
                # Manejar PDFs
                if file['mimeType'] == 'application/pdf':
                    request = service.files().get_media(fileId=file['id'])
                    file_data = io.BytesIO()
                    downloader = MediaIoBaseDownload(file_data, request)
                    
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    file_data.seek(0)
                    pdf_reader = PdfReader(file_data)
                    
                    # Extraer texto de todas las páginas
                    for page_num, page in enumerate(pdf_reader.pages):
                        content += f"\n--- Página {page_num + 1} ---\n"
                        content += page.extract_text()
                    
                    print(f"   ✓ PDF procesado: {len(pdf_reader.pages)} páginas")
                
                # Manejar Google Docs
                elif file['mimeType'] == 'application/vnd.google-apps.document':
                    # Exportar como texto plano
                    request = service.files().export_media(
                        fileId=file['id'],
                        mimeType='text/plain'
                    )
                    file_data = io.BytesIO()
                    downloader = MediaIoBaseDownload(file_data, request)
                    
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    content = file_data.getvalue().decode('utf-8')
                    print(f"   ✓ Google Doc exportado como texto")
                
                # Manejar archivos de Word (.docx)
                elif file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    request = service.files().get_media(fileId=file['id'])
                    file_data = io.BytesIO()
                    downloader = MediaIoBaseDownload(file_data, request)
                    
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    # Para .docx necesitaríamos python-docx
                    print(f"   ⚠ Archivo .docx - requiere procesamiento adicional")
                    content = "[Archivo .docx - contenido binario]"
                
                else:
                    print(f"   ⚠ Tipo de archivo no soportado: {file['mimeType']}")
                    continue
                
                # Crear documento
                doc = {
                    'name': file['name'],
                    'id': file['id'],
                    'mimeType': file['mimeType'],
                    'content': content,
                    'size': len(content)
                }
                documents.append(doc)
                
                # Mostrar preview
                preview_length = min(200, len(content))
                if preview_length > 0:
                    preview = content[:preview_length].replace('\n', ' ').strip()
                    print(f"   - Tamaño: {len(content)} caracteres")
                    print(f"   - Preview: {preview}...")
                
                print()
                
            except Exception as e:
                print(f"   ❌ Error procesando archivo: {str(e)}")
                print()
                continue
        
        # Resumen final
        print(f"\n{'='*80}")
        print(f"RESUMEN: Se procesaron {len(documents)} documento(s) exitosamente")
        print(f"{'='*80}\n")
        
        for i, doc in enumerate(documents, 1):
            print(f"{i}. {doc['name']}")
            print(f"   - Tipo: {doc['mimeType']}")
            print(f"   - Contenido: {doc['size']} caracteres")
            print()
        
        return documents
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    documents = download_and_process_files(folder_id)
