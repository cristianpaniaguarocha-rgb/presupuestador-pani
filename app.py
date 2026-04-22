import streamlit as st
import pandas as pd
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Pani Presupuestos", layout="wide")

# --- CONEXIÓN GOOGLE SHEETS ---
SHEET_ID = "1lZrBwlLW8er9d6VexvMI0nqhnpuwos0O3caWTVRqdfU"
@st.cache_data
def load_prices():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
    return pd.read_csv(url)

try:
    df = load_prices()
    st.success("✅ Base de datos de Málaga conectada")
except:
    st.error("❌ Error al conectar con el Sheets")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Pegá tu API Key acá", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    st.info("Usando modelo: Gemini 2.5 Flash")

# --- APP PRINCIPAL ---
st.title("🏗️ Pani Presupuestos")
uploaded_file = st.file_uploader("Subí el diseño de SketchUp o foto", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 Analizar Cocina"):
        if not api_key:
            st.error("Falta la API Key en el menú lateral")
        else:
            try:
                # USANDO EL MODELO QUE VIMOS EN TU LISTA
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                
                prompt = """
                Sos un experto en montaje de cocinas. Analizá esta imagen y hacé un listado de:
                1. Muebles bajos (especificá si son cajoneras o puertas).
                2. Muebles altos.
                3. Columnas (Horno, Micro, Frigo).
                Danos las medidas estimadas en cm según lo que veas.
                """
                
                response = model.generate_content([prompt, img])
                
                st.subheader("📋 Despiece Sugerido:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")

# --- CHECKLIST PÁGINA 3 PDF ---
st.divider()
st.header("🛠️ Checklist de Seguridad")
c1, c2 = st.columns(2)
with c1:
    st.checkbox("Patas (Bolsas x4)")
    st.checkbox("Zócalos Aluminio")
    st.checkbox("Copetes")
with c2:
    st.checkbox("Bisagras 180° / Rincón")
    st.checkbox("Cajones Plastimodul")
    st.checkbox("Mano de Obra")
