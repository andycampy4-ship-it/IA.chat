# main.py
import requests
import os
from memoria import cargar_historial, guardar_historial

# Historial persistente
historial = cargar_historial()
url = "http://localhost:11434/api/generate"  # URL de tu modelo Phi

# Configuración para resúmenes automáticos
MAX_MENSAJES = 30  # número máximo de mensajes antes de resumir

# ----------------------------
# Función para cargar personalidad
# ----------------------------
def cargar_personalidad(nombre):
    """
    Carga el prompt base desde un archivo en la carpeta prompts.
    nombre: 'chistosa', 'matematicas', 'coach', etc.
    """
    ruta = os.path.join("prompts", f"{nombre}.py")
    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()
    contexto = {}
    exec(codigo, contexto)  # ejecuta el código para obtener la variable 'sistema'
    return contexto["sistema"]

# ----------------------------
# Función para resumir historial
# ----------------------------
def resumir_historial(historial, modelo_url=url):
    """
    Usa Phi para resumir el historial cuando sea muy largo.
    Devuelve un historial resumido como lista de un solo mensaje 'Sistema'.
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

    r = requests.post(modelo_url, json={"model": "phi", "prompt": prompt_resumen, "stream": False})
    resumen = r.json()["response"]

    return [{"rol": "Sistema", "mensaje": resumen}]

# ----------------------------
# Función principal de la IA
# ----------------------------
def preguntar(prompt, sistema):
    """
    Envía el mensaje del usuario a Phi y devuelve la respuesta de la IA.
    Incluye memoria persistente y resumen automático.
    """
    global historial
    historial.append({"rol": "Usuario", "mensaje": prompt})

    # Resumir si hay demasiados mensajes
    if len(historial) > MAX_MENSAJES:
        historial = resumir_historial(historial)

    # Construir prompt completo para la IA
    conversacion = sistema + "\n"
    for item in historial:
        conversacion += f'{item["rol"]}: {item["mensaje"]}\n'
    conversacion += "IA:"

    # Llamar al modelo Phi
    r = requests.post(url, json={"model": "phi", "prompt": conversacion, "stream": False})
    respuesta = r.json()["response"]

    historial.append({"rol": "IA", "mensaje": respuesta})
    guardar_historial(historial)  # guardar en disco
    return respuesta

# ----------------------------
# Prueba en consola (opcional)
# ----------------------------
if __name__ == "__main__":
    personalidad = input("Elige personalidad (chistosa/matematicas/coach): ")
    sistema = cargar_personalidad(personalidad)
    while True:
        pregunta = input("Tu: ")
        print("IA:", preguntar(pregunta, sistema))