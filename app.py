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
                # Esta es la forma más moderna de llamar al modelo
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content([
                    "Sos un experto carpintero. Listá los muebles de esta cocina para un presupuesto.", 
                    img
                ])
                st.subheader("Resultado:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")

# --- CHECKLIST ---
st.divider()
st.header("📋 Checklist de Seguridad")
opciones = ["Patas", "Zócalos", "Copetes", "Bisagras", "Tiradores", "Mano de Obra"]
for opt in opciones:
    st.checkbox(opt)
