import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import qrcode
from datetime import date

st.title("Generador de Certificados - RUAM")
st.subheader("Dirección General de Desarrollo Minero")

with st.form("formulario_certificado"):
    nro_productor = st.text_input("Productor Minero N.º")
    titular = st.text_input("Titular (Empresa/Persona)")
    cantera = st.text_input("Nombre de la Cantera")
    mineral = st.text_input("Mineral (Ej: Extracción de Arena Silícea)")
    domicilio = st.text_input("Domicilio Legal")
    vig_ruam = st.date_input("Vigencia RUAM")
    vig_ambiente = st.date_input("Vigencia Certificado Aptitud Ambiental")
    
    submit = st.form_submit_button("Generar Certificado")

if submit:
    # 1. Cargar la plantilla
    doc = DocxTemplate("plantilla_ruam.docx")
    
    # 2. Generar el contenido del código QR
    datos_qr = f"RUAM - Productor: {nro_productor} | Titular: {titular} | Vencimiento: {vig_ruam.strftime('%d/%m/%Y')}"
    
    # 3. Crear la imagen del código QR
    qr = qrcode.make(datos_qr)
    qr_buffer = io.BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    
    # 4. Convertir el QR a un formato que docxtpl pueda insertar (tamaño: 35 milímetros)
    imagen_qr = InlineImage(doc, qr_buffer, width=Mm(35))
    fecha_hoy = date.today().strftime("%d/%m/%Y")
    
    # 5. Mapear los datos
    contexto = {
        "nro_productor": nro_productor,
        "titular": titular,
        "cantera": cantera,
        "mineral": mineral,
        "domicilio": domicilio,
        "vig_ruam": vig_ruam.strftime("%d/%m/%Y"),
        "vig_ambiente": vig_ambiente.strftime("%d/%m/%Y"),
        "qr_code": imagen_qr,  # Coma agregada aquí
        "fecha_emision": fecha_hoy
    }
    
    # 6. Renderizar y guardar
    doc.render(contexto)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    st.success("¡Certificado generado con éxito con su Código QR!")
    
    st.download_button(
        label="Descargar Certificado (Word)",
        data=buffer,
        file_name=f"Certificado_{titular}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )