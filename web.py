# web.py
import streamlit as st
from main import preguntar, cargar_personalidad

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(page_title="IA Local Phi", page_icon="🤖", layout="wide")

# ----------------------------
# Selector de personalidad
# ----------------------------
personalidad = st.selectbox(
    "Elige la personalidad de tu IA:",
    ["chistosa", "matematicas", "coach"]
)
sistema = cargar_personalidad(personalidad)

# ----------------------------
# Inicializar historial en la sesión
# ----------------------------
if "historial" not in st.session_state:
    st.session_state.historial = []

# ----------------------------
# Entrada de usuario
# ----------------------------
entrada = st.text_input("Escribe tu mensaje:")

# Botón para enviar
if st.button("Enviar") and entrada.strip() != "":
    respuesta = preguntar(entrada, sistema)
    st.session_state.historial.append(("Tu", entrada))
    st.session_state.historial.append(("IA", respuesta))

# ----------------------------
# Mostrar conversación en burbujas
# ----------------------------
for quien, mensaje in st.session_state.historial:
    color = "#1f77b4" if quien == "Tu" else "#ff7f0e"
    st.markdown(
        f'<div style="background:#f0f0f5; padding:10px; margin-bottom:5px; border-radius:10px; color:{color};"><b>{quien}:</b> {mensaje}</div>',
        unsafe_allow_html=True
    )

# ----------------------------
# Sección lateral con tips
# ----------------------------
with st.sidebar:
    st.markdown("### Tips")
    st.markdown("- Haz preguntas claras y cortas.")
    st.markdown("- La IA recuerda lo que escribes entre sesiones.")
    st.markdown("- Cambia la personalidad usando el menú desplegable.")

    st.markdown("- La conversación larga se resume automáticamente para mantener la IA rápida.")
