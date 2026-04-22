import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Pani Presupuestos - Málaga", layout="wide")

st.title("🏗️ Pani-Presupuestos v1.0")
st.write("Herramienta profesional para presupuestos de cocina en Málaga.")

# --- CONEXIÓN CON TU GOOGLE SHEET ---
# Usamos el ID de tu documento que me pasaste
SHEET_ID = "1lZrBwlLW8er9d6VexvMI0nqhnpuwos0O3caWTVRqdfU"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data
def load_prices(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# GIDs de tus pestañas (se sacan de la URL de cada pestaña en el navegador)
# Por ahora cargamos la principal, pero esto se expande a las 4.
try:
    df_modulos = load_prices("0") # La primera pestaña suele ser 0
    st.success("✅ Base de datos conectada con éxito")
except:
    st.error("❌ Error al conectar con Google Sheets. Revisa el ID y permisos.")

# --- SIDEBAR: CONFIGURACIÓN Y API KEY ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    
    st.divider()
    st.subheader("Datos del Cliente")
    cliente_nom = st.text_input("Nombre Cliente")
    cliente_tel = st.text_input("Teléfono")

# --- ZONA DE CARGA DE IMAGEN ---
st.header("1. Captura de la Cocina")
uploaded_file = st.file_uploader("Sube el diseño de SketchUp o una foto real", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Vista de la cocina", use_container_width=True)
    
    if st.button("🚀 Analizar con IA"):
        if not api_key:
            st.warning("Por favor, introduce la API Key en el menú lateral.")
        else:
            with st.spinner("Gemini está contando los muebles..."):
                # Aquí configuramos a Gemini 1.5 Pro
               model = genai.GenerativeModel('models/gemini-1.5-flash')
                prompt = """Analiza esta imagen técnica de una cocina. 
                Necesito que listes los módulos de izquierda a derecha. 
                Diferencia entre: Mueble bajo cajonera, Mueble bajo puerta, Lavadora, Fregadero, Columna Horno y Muebles Altos.
                Sé muy preciso con los cajones. Devuelve una lista técnica."""
                
                response = model.generate_content([prompt, img])
                st.subheader("2. Despiece detectado (Editable)")
                st.write(response.text)

# --- ZONA DE EDICIÓN Y CHECKLIST (SIMULADO) ---
st.divider()
st.header("3. Checklist de Seguridad (Pág. 3 PDF)")
col1, col2 = st.columns(2)

with col1:
    st.checkbox("Patas (Bolsas x4)")
    st.checkbox("Zócalo Aluminio (ML)")
    st.checkbox("Pinzas de zócalo")
    st.checkbox("Copete y accesorios")

with col2:
    st.checkbox("Bisagras (Normal/Rincón)")
    st.checkbox("Tiradores")
    st.checkbox("Fregadero y Grifo")
    st.checkbox("Mano de Obra Montaje")

# --- BOTÓN FINAL ---
if st.button("📄 Generar Borrador de Presupuesto"):
    st.balloons()
    st.info("Aquí se generará el Google Doc detallado y resumido en tu Drive.")
