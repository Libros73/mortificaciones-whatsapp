import json
import random
import requests
import os  # Importar módulo para leer variables de entorno

# Obtener credenciales desde GitHub Secrets
PHONE_NUMBER = os.getenv("WHATSAPP_NUMBER")
API_KEY = os.getenv("CALLMEBOT_APIKEY")

# Cargar las mortificaciones desde el JSON
with open("mortificaciones.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Mortificaciones constantes (puedes cambiarlas si quieres)
MORTIFICACIONES_FIJAS = [
    "Ayunar los viernes.",
    "Orar el Rosario todos los días."
]

# Seleccionar 3 mortificaciones aleatorias de diferentes categorías
mortificaciones_aleatorias = []
categorias = list(data["mortificaciones"])
random.shuffle(categorias)

for categoria in categorias:
    acciones = categoria["acciones"]
    if acciones:
        mortificacion = random.choice(acciones)
        if mortificacion not in MORTIFICACIONES_FIJAS:
            mortificaciones_aleatorias.append(mortificacion)
    if len(mortificaciones_aleatorias) == 3:
        break

# Crear el mensaje final
mensaje = "Mortificaciones del día:\n\n"
mensaje += f"1️⃣ {MORTIFICACIONES_FIJAS[0]}\n"
mensaje += f"2️⃣ {MORTIFICACIONES_FIJAS[1]}\n"
mensaje += f"3️⃣ {mortificaciones_aleatorias[0]}\n"
mensaje += f"4️⃣ {mortificaciones_aleatorias[1]}\n"
mensaje += f"5️⃣ {mortificaciones_aleatorias[2]}\n"

# Enviar el mensaje por WhatsApp
url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE_NUMBER}&text={mensaje}&apikey={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Mensaje enviado con éxito")
else:
    print(f"❌ Error al enviar el mensaje: {response.status_code}")
