# main.py
import requests
import os

# ----------------------------
# Configuración modelo remoto
# ----------------------------
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODELO_URL = "https://api-inference.huggingface.co/models/gpt2"  # modelo gratuito de ejemplo
MAX_MENSAJES = 30  # número máximo de mensajes antes de resumir

# Historial global (en la nube usar session_state)
historial = []

# ----------------------------
# Cargar personalidad
# ----------------------------
def cargar_personalidad(nombre):
    """
    Carga el archivo de personalidad que está en la raíz del repo
    nombre: 'chistosa', 'matematicas', 'coach'
    """
    ruta = f"{nombre}.py"
    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()
    contexto = {}
    exec(codigo, contexto)  # ejecuta el código para obtener la variable 'sistema'
    return contexto["sistema"]

# ----------------------------
# Resumen automático del historial
# ----------------------------
def resumir_historial(historial):
    """
    Resume la conversación si se hace muy larga.
    Devuelve un historial reducido como lista de un solo mensaje 'Sistema'.
    """
    conversacion = ""
    for item in historial:
        conversacion += f'{item["rol"]}: {item["mensaje"]}\n'

    prompt_resumen = f"""
Resume la siguiente conversación de manera breve y clara,
conservando solo la información importante sobre el usuario y el contexto de la conversación.
Conversación:
{conversacion}
Resumen:
"""

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    r = requests.post(MODELO_URL, headers=headers, json={"inputs": prompt_resumen})
    resumen = r.json()[0]["generated_text"]

    return [{"rol": "Sistema", "mensaje": resumen}]

# ----------------------------
# Función principal de la IA
# ----------------------------
def preguntar(prompt, sistema):
    """
    Envía el mensaje del usuario al modelo remoto y devuelve la respuesta de la IA.
    Incluye memoria (historial) y resumen automático.
    """
    global historial
    historial.append({"rol": "Usuario", "mensaje": prompt})

    # Resumir si hay demasiados mensajes
    if len(historial) > MAX_MENSAJES:
        historial = resumir_historial(historial)

    # Construir prompt completo
    conversacion = sistema + "\n"
    for item in historial:
        conversacion += f'{item["rol"]}: {item["mensaje"]}\n'
    conversacion += "IA:"

    # Llamar al modelo remoto
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    r = requests.post(MODELO_URL, headers=headers, json={"inputs": conversacion})
    respuesta = r.json()[0]["generated_text"]

    historial.append({"rol": "IA", "mensaje": respuesta})
    return respuesta

# ----------------------------
# Prueba en consola (opcional)
# ----------------------------
if __name__ == "__main__":
    personalidad = input("Elige personalidad (chistosa/matematicas/coach): ")
    sistema = cargar_personalidad(personalidad)
    while True:
        pregunta_usuario = input("Tu: ")
        print("IA:", preguntar(pregunta_usuario, sistema))
