import streamlit as st
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import io
import qrcode
from datetime import date

# --- 1. SISTEMA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.title("🔒 Acceso Restringido")
    st.subheader("Sistema de Emisión RUAM")
    
    usuario = st.text_input("Usuario")
    contrasena = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        if usuario == "admin" and contrasena == "123456": 
            st.session_state['autenticado'] = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

# --- 2. APLICACIÓN PRINCIPAL ---
if st.session_state['autenticado']:
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()
        
    st.title("Generador de Certificados - RUAM")
    st.subheader("Dirección General de Desarrollo Minero")

    with st.form("formulario_certificado"):
        nro_productor = st.text_input("Productor Minero N.º")
        titular = st.text_input("Titular (Empresa/Persona)")
        cantera = st.text_input("Nombre de la Cantera")
        mineral = st.text_input("Mineral (Ej: Extracción de Arena Silícea)")
        
        # --- AQUÍ ESTÁ EL NUEVO CAMPO DE ACTIVIDAD ---
        actividad = st.text_input("Actividad (Ej: Explotación de cantera en dominio particular)")
        
        domicilio = st.text_input("Domicilio Legal")
        vig_ruam = st.date_input("Vigencia RUAM")
        vig_ambiente = st.date_input("Vigencia Certificado Aptitud Ambiental")
        
        submit = st.form_submit_button("Generar Certificado")

    if submit:
        doc = DocxTemplate("plantilla_ruam.docx")
        
        datos_qr = f"RUAM - Productor: {nro_productor} | Titular: {titular} | Vencimiento: {vig_ruam.strftime('%d/%m/%Y')}"
        
        qr = qrcode.make(datos_qr)
        qr_buffer = io.BytesIO()
        qr.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        imagen_qr = InlineImage(doc, qr_buffer, width=Mm(35))
        fecha_hoy = date.today().strftime("%d/%m/%Y")
        
        # --- AQUÍ SE MAPEA LA ACTIVIDAD PARA ENVIARLA AL WORD ---
        contexto = {
            "nro_productor": nro_productor,
            "titular": titular,
            "cantera": cantera,
            "mineral": mineral,
            "actividad": actividad,
            "domicilio": domicilio,
            "vig_ruam": vig_ruam.strftime("%d/%m/%Y"),
            "vig_ambiente": vig_ambiente.strftime("%d/%m/%Y"),
            "qr_code": imagen_qr,
            "fecha_emision": fecha_hoy
        }
        
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
