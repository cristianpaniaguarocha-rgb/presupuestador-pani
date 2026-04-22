import streamlit as st
import google.generativeai as genai

st.title("Prueba de Conexión Pani")

# Entrada de clave
api_key = st.text_input("Pegá tu API Key acá", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Listamos los modelos disponibles para ver qué ve tu clave
        modelos = [m.name for m in genai.list_models()]
        st.success("✅ ¡Tu API Key funciona!")
        st.write("Modelos disponibles en tu cuenta:")
        st.write(modelos)
    except Exception as e:
        st.error(f"❌ Error con la API Key: {e}")
