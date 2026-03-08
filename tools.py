# web.py
import streamlit as st
from main import preguntar

st.title("Mi IA local con Phi")

if "historial" not in st.session_state:
    st.session_state.historial = ""

entrada = st.text_input("Escribe algo:")

if st.button("Enviar"):
    respuesta = preguntar(entrada)
    st.session_state.historial += f"Tu: {entrada}\nIA: {respuesta}\n"
    st.text_area("Conversación", st.session_state.historial, height=300)