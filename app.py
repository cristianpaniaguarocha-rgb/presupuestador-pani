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
    st.success("✅ Conectado a Málaga")
except:
    st.error("❌ Error Sheets")

# --- SIDEBAR ---
with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# --- APP PRINCIPAL ---
st.title("🏗️ Pani Presupuestos")
uploaded_file = st.file_uploader("Foto de la cocina", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 Analizar"):
        if not api_key:
            st.error("Falta la API Key")
        else:
            try:
                # LA SOLUCIÓN: Usar el método generativo directo
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # En las versiones nuevas, se recomienda pasar la imagen así
                response = model.generate_content(
                    contents=[
                        "Sos un experto carpintero. Listá los muebles de esta cocina para un presupuesto detallado.",
                        img
                    ]
                )
                
                st.subheader("Resultado:")
                if response.text:
                    st.write(response.text)
                else:
                    st.warning("La IA no devolvió texto. Revisa la imagen.")
                    
            except Exception as e:
                # Si esto falla, probamos el último recurso de nombre
                st.info("Reintentando con ruta alternativa...")
                try:
                    model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
                    res = model_alt.generate_content(["Analiza la cocina", img])
                    st.write(res.text)
                except:
                    st.error(f"Error técnico persistente: {e}")

# --- CHECKLIST (Basado en tu PDF) ---
st.divider()
st.header("📋 Checklist de Seguridad")
# Sacado de tu despiece página 3
col1, col2 = st.columns(2)
with col1:
    st.checkbox("Patas (Bolsa x4)") # [cite: 77]
    st.checkbox("Zócalo y Pinzas") # [cite: 50, 51]
    st.checkbox("Copete (Rinconero/Esquinero)") # [cite: 58, 59, 60]
with col2:
    st.checkbox("Bisagras (Normal/180°)") # [cite: 75, 76]
    st.checkbox("Cajones Plastimodul") # [cite: 65]
    st.checkbox("Mano de Obra (M.O.)") # [cite: 41]
