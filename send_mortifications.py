import json
import random
import requests
import os
import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales desde GitHub Secrets
PHONE_NUMBER = "573058180027"
API_KEY = "5298266"

# Verificar que las credenciales existen
if not PHONE_NUMBER[0] or not API_KEY:
    print("Error: No se encontraron las credenciales necesarias")
    print("Asegúrate de configurar WHATSAPP_NUMBER y CALLMEBOT_APIKEY en los secrets de GitHub")
    exit()

# Definir mortificaciones fijas por día de la semana
MORTIFICACIONES_FIJAS = {
    "Monday": ["No tomar café", "Hacer 10 minutos de oración en silencio"],
    "Tuesday": ["No comer dulces", "Leer un capítulo de la Biblia"],
    "Wednesday": ["No usar redes sociales por una hora", "Hacer un acto de caridad"],
    "Thursday": ["Tomar agua en lugar de gaseosas", "Evitar quejarse todo el día"],
    "Friday": ["Hacer ayuno parcial", "Rezar el Viacrucis"],
    "Saturday": ["Hacer una visita al Santísimo", "No ver televisión"],
}

# Obtener el día de la semana actual
hoy = datetime.datetime.now().strftime("%A")

# Si es domingo, no se envía nada
if hoy == "Sunday":
    print("Hoy es domingo, no se envían mortificaciones.")
    exit()

# Cargar las mortificaciones desde el JSON
try:
    with open("mortificaciones.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: No se encontró el archivo mortificaciones.json")
    exit()

# Seleccionar 3 mortificaciones aleatorias
mortificaciones_aleatorias = []
categorias = list(data["mortificaciones"])
random.shuffle(categorias)

for categoria in categorias:
    acciones = categoria["acciones"]
    if acciones:
        mortificacion = random.choice(acciones)
        if mortificacion not in MORTIFICACIONES_FIJAS[hoy]:  # Evita duplicados
            mortificaciones_aleatorias.append(mortificacion)
    if len(mortificaciones_aleatorias) == 3:
        break

# Crear el mensaje final
mensaje = f"Mortificaciones del {hoy}:\n\n"
mensaje += f"1️⃣ {MORTIFICACIONES_FIJAS[hoy][0]}\n"
mensaje += f"2️⃣ {MORTIFICACIONES_FIJAS[hoy][1]}\n"
mensaje += f"3️⃣ {mortificaciones_aleatorias[0]}\n"
mensaje += f"4️⃣ {mortificaciones_aleatorias[1]}\n"
mensaje += f"5️⃣ {mortificaciones_aleatorias[2]}\n"

# Enviar el mensaje a cada número
for phone in PHONE_NUMBER:
    if phone:  # Verificar que el número no está vacío
        # Codificar el mensaje para la URL
        mensaje_codificado = requests.utils.quote(mensaje)
        url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={mensaje_codificado}&apikey={API_KEY}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ Mensaje enviado a {phone}")
            else:
                print(f"❌ Error al enviar el mensaje a {phone}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en la conexión: {e}")

# Imprimir el mensaje para verificación
print("\nMensaje enviado:")
print(mensaje)
