import os
import json
import io
from datetime import datetime
from pathlib import Path

import streamlit as st
from models.cv_models import AnalisisCV
from services.pdf_procesor import extraer_texto_pdf
from services.cv_evaluator import evaluar_candidato

# ReportLab para generar PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- Configuración y Constantes ---
OUTPUT_DIR = Path("resultados_cv")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Funciones de Utilidad ---

def generar_pdf_bytes(resultado: AnalisisCV) -> io.BytesIO:
    """Genera el PDF en un buffer de memoria para descarga directa."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para títulos
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor("#1E3A8A")
    )

    contenido = []
    contenido.append(Paragraph("Informe de Evaluación de Candidato", title_style))
    contenido.append(Spacer(1, 12))
    
    # Tabla de datos básicos
    datos = [
        ["Candidato:", resultado.nombre_candidato],
        ["Ajuste:", f"{resultado.porcentaje_ajuste}%"],
        ["Experiencia:", f"{resultado.experiencia_laboral} años"],
        ["Educación:", resultado.educacion]
    ]
    t = Table(datos, colWidths=[100, 350])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    contenido.append(t)
    contenido.append(Spacer(1, 15))

    # Secciones
    secciones = [
        ("🛠️ Habilidades Clave", ", ".join(resultado.habilidades_clave)),
        ("💪 Fortalezas", "<br/>".join(resultado.fortalezas)),
        ("📈 Áreas de Mejora", "<br/>".join(resultado.areas_mejora)),
        ("💼 Experiencia Relevante", resultado.experiencia_relevante)
    ]

    for titulo, texto in secciones:
        contenido.append(Paragraph(f"<b>{titulo}</b>", styles["Heading2"]))
        contenido.append(Paragraph(texto or "N/A", styles["Normal"]))
        contenido.append(Spacer(1, 10))

    # Recomendación Final
    rec_color = colors.green if resultado.porcentaje_ajuste >= 70 else colors.red
    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph("<b>Recomendación Final:</b>", styles["Heading2"]))
    rec_text = "APTO PARA EL PUESTO" if resultado.porcentaje_ajuste >= 70 else "NO RECOMENDADO"
    contenido.append(Paragraph(rec_text, ParagraphStyle('Rec', parent=styles['Normal'], textColor=rec_color, fontWeight='bold')))

    doc.build(contenido)
    buffer.seek(0)
    return buffer

def guardar_localmente(resultado: AnalisisCV):
    """Guarda una copia en el servidor/PC local."""
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(x for x in resultado.nombre_candidato if x.isalnum() or x in "._- ").replace(" ", "_")
    base_path = OUTPUT_DIR / f"{safe_name}_{fecha_str}"
    
    # Guardar JSON
    with open(f"{base_path}.json", "w", encoding="utf-8") as f:
        json.dump(resultado.__dict__, f, ensure_ascii=False, indent=4)
    
    # Guardar PDF
    pdf_data = generar_pdf_bytes(resultado)
    with open(f"{base_path}.pdf", "wb") as f:
        f.write(pdf_data.read())
    
    return f"{base_path}.json", f"{base_path}.pdf"

# --- Interfaz Streamlit ---

def main():
    st.set_page_config(page_title="AI CV Analyzer", page_icon="🎯", layout="wide")
    
    st.title("🎯 AI CV Analyzer Pro")
    st.caption("Evaluación inteligente de talento mediante procesamiento de lenguaje natural")

    # Inicialización de estado
    if "resultado_analisis" not in st.session_state:
        st.session_state.resultado_analisis = None

    col_in, col_out = st.columns([1, 1.2], gap="large")

    with col_in:
        st.header("📋 Configuración")
        
        archivo_cv = st.file_uploader("1. Cargar CV (PDF)", type=['pdf'])
        
        desc_puesto = st.text_area(
            "2. Descripción del puesto",
            height=300,
            placeholder="Pega aquí los requisitos y responsabilidades..."
        )

        btn_analizar = st.button("🔍 Iniciar Análisis", type="primary", use_container_width=True)
        
        if st.button("🗑️ Limpiar Todo", use_container_width=True):
            st.session_state.resultado_analisis = None
            st.rerun()

    with col_out:
        st.header("📊 Resultados")
        
        if btn_analizar:
            if not archivo_cv or not desc_puesto:
                st.error("⚠️ Falta el CV o la descripción del puesto.")
            else:
                procesar_flujo_analisis(archivo_cv, desc_puesto)
        
        elif st.session_state.resultado_analisis:
            mostrar_resultados(st.session_state.resultado_analisis)
        
        else:
            st.info("Complete los datos de la izquierda y haga clic en 'Iniciar Análisis'.")

def procesar_flujo_analisis(archivo, descripcion):
    with st.status("Procesando información...", expanded=True) as status:
        st.write("Reading PDF...")
        texto_cv = extraer_texto_pdf(archivo)
        
        if "Error" in texto_cv:
            st.error(texto_cv)
            return

        st.write("Consultando a la IA...")
        resultado = evaluar_candidato(texto_cv, descripcion)
        st.session_state.resultado_analisis = resultado
        status.update(label="¡Análisis completado!", state="complete", expanded=False)
    
    st.rerun()

def mostrar_resultados(res: AnalisisCV):
    # Métricas principales
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Ajuste al Puesto", f"{res.porcentaje_ajuste}%")
    with m2:
        # Lógica de color de recomendación
        color = "green" if res.porcentaje_ajuste >= 70 else "orange" if res.porcentaje_ajuste >= 50 else "red"
        st.markdown(f"### Estado: :{color}[{ 'RECOMENDADO' if res.porcentaje_ajuste >= 70 else 'EVALUAR'}]")

    with st.expander("👤 Información del Candidato", expanded=True):
        st.write(f"**Nombre:** {res.nombre_candidato}")
        st.write(f"**Años de Experiencia:** {res.experiencia_laboral}")
        st.write(f"**Educación:** {res.educacion}")

    st.subheader("💼 Experiencia Relevante")
    st.info(f"📋 **Resumen de experiencia:**\n\n{res.experiencia_relevante}")

    st.subheader("🛠️ Habilidades Clave")
    st.write(" ".join([f"`{h}`" for h in res.habilidades_clave]))

    c1, c2 = st.columns(2)
    with c1:
        st.success("✅ **Fortalezas**")
        for f in res.fortalezas: st.markdown(f"- {f}")
    with c2:
        st.warning("📈 **Áreas de Mejora**")
        for a in res.areas_mejora: st.markdown(f"- {a}")

    st.divider()
    
    # Acciones de descarga
    st.subheader("💾 Exportar Informe")
    col_d1, col_d2 = st.columns(2)
    
    pdf_buffer = generar_pdf_bytes(res)
    
    with col_d1:
        st.download_button(
            label="📥 Descargar PDF",
            data=pdf_buffer,
            file_name=f"Evaluacion_{res.nombre_candidato}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    with col_d2:
        if st.button("📁 Guardar en Servidor", use_container_width=True):
            r_json, r_pdf = guardar_localmente(res)
            st.toast(f"Guardado en: {OUTPUT_DIR}", icon="💾")

if __name__ == "__main__":
    main()