import json
import os

ARCHIVO = "historial.json"

# Cargar historial si existe
def cargar_historial():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Guardar historial
def guardar_historial(historial):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=2)