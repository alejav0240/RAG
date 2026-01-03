import PyPDF2
from io import BytesIO

def extraer_texto_pdf(archivo_pdf: bytes):
    
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_pdf.read()))
        texto_completo = ""

        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            # texto += f"Pagina {numero_pagina}:\n"
            texto_pagina = pagina.extract_text()
            if texto_pagina.strip():
                texto_completo += f"\n--- Pagina {numero_pagina}:\n" + texto_pagina + "\n"

        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "ERROR: EL PDF parece estar vacio o contiene solo imagenes"

        return texto_completo

    except Exception as e:
        print(f"Error al extraer texto del PDF: {str(e)}")
        return None