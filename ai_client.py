import time
import getpass
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests
from colorama import Fore, Style, init

# Inicializamos colorama para que los colores funcionen
init(autoreset=True)

# 1. Funcion de login
def login_usuario():
    print(f"\n{Fore.CYAN}--- login de usuario ---")
    email = input(f"{Fore.YELLOW}Email: {Style.RESET_ALL}")
    password = getpass.getpass(f"{Fore.YELLOW}Contraseña: {Style.RESET_ALL}")

    url_login = "http://127.0.0.1:8000/api/auth/login/"

    try:
        response = requests.post(
            url_login,
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            print(f"{Fore.GREEN}Usuario loggeado correctamente")
            return response.json().get("Token")

        print(f"{Fore.RED}Error: {response.json().get('error')}")

    except Exception as e:
        print(f"{Fore.RED}Error de conexion:", e)

    return None

# 2. Funcion de herramienta (Modificada para la IA)
def consultar_mis_tareas():
    """
    Consulta la lista de eventos o tareas del usuario autenticado en la API.
    No requiere argumentos.
    """
    global token 
    
    print(f"\n{Fore.MAGENTA}[SISTEMA]: La IA está consultando la API de eventos...{Style.RESET_ALL}")
    url = "http://127.0.0.1:8000/api/eventos/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            return {"error": f"Servidor respondió con {res.status_code}", "detalle": res.text}
    except Exception as e:
        return {"error": str(e)}
    
def crear_nuevo_evento(titulo: str, descripcion: str, fecha: str, lugar: str):
    """
    Crea un nuevo evento. 
    Argumentos:
        titulo: Nombre del evento.
        descripcion: Detalles de qué trata.
        fecha: Fecha en formato texto (ej: 2026-03-20).
        lugar: Ubicación física.
    """
    global token
    print(f"\n{Fore.MAGENTA}[SISTEMA]: La IA está ejecutando 'crear_nuevo_evento' para: {titulo}{Style.RESET_ALL}")
    
    url = "http://127.0.0.1:8000/api/eventos/"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha": fecha,
        "lugar": lugar
    }

    try:
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 201:
            return {"resultado": "Éxito", "detalle": "Evento creado correctamente"}
        else:
            return {"resultado": "Error", "detalle": res.json()}
    except Exception as e:
        return {"resultado": "Error de conexión", "detalle": str(e)}
    
def actualizar_evento(id_evento: str, titulo: str = None, descripcion: str = None, fecha: str = None, lugar: str = None):
    """
    Actualiza los datos de un evento existente usando su ID de Firebase.
    Argumentos:
        id_evento: El ID alfanumérico del evento (ej: 'OZvDgeu...').
        titulo: (Opcional) Nuevo nombre.
        descripcion: (Opcional) Nuevos detalles.
        fecha: (Opcional) Nueva fecha en formato YYYY-MM-DD.
        lugar: (Opcional) Nueva ubicación.
    """
    global token
    print(f"\n{Fore.MAGENTA}[SISTEMA]: La IA está actualizando el evento ID: {id_evento}...{Style.RESET_ALL}")
    
    url = f"http://127.0.0.1:8000/api/eventos/{id_evento}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {}
    if titulo: payload["titulo"] = titulo
    if descripcion: payload["descripcion"] = descripcion
    if fecha: payload["fecha"] = fecha
    if lugar: payload["lugar"] = lugar

    if not payload:
        return {"resultado": "Error", "detalle": "No se proporcionaron campos para actualizar."}

    try:
        res = requests.patch(url, json=payload, headers=headers)
        if res.status_code == 200:
            return {"resultado": "Éxito", "detalle": "Evento actualizado correctamente en Firebase."}
        else:
            return {"resultado": "Error", "detalle": res.json()}
    except Exception as e:
        return {"resultado": "Error de conexión", "detalle": str(e)}
    
def eliminar_evento(id_evento: str):
    """
    Elimina permanentemente un evento del sistema usando su ID de Firebase.
    Argumentos:
        id_evento: El ID alfanumérico del evento a borrar.
    """
    global token
    print(f"\n{Fore.MAGENTA}[SISTEMA]: La IA está eliminando el evento ID: {id_evento}...{Style.RESET_ALL}")
    
    url = f"http://127.0.0.1:8000/api/eventos/{id_evento}/"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.delete(url, headers=headers)
        if res.status_code == 204 or res.status_code == 200:
            return {"resultado": "Éxito", "detalle": "El evento ha sido eliminado."}
        else:
            return {"resultado": "Error", "detalle": "No se pudo eliminar el evento."}
    except Exception as e:
        return {"resultado": "Error de conexión", "detalle": str(e)}
    
# 3. Configuracion de la IA

load_dotenv(dotenv_path='proyecto_advaih/.env')
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
modelo_id = "gemini-1.5-flash" # Cambiado a 1.5 para evitar error de cuota

# 4. Flujo de la lógica
token = login_usuario()

if token:
    print(f"\n{Fore.BLUE}IA: Hola, soy tu agente. ¿En qué puedo ayudarte hoy?")

    chat = client.chats.create(
        model=modelo_id,
        config=types.GenerateContentConfig(
            tools=[consultar_mis_tareas, crear_nuevo_evento, actualizar_evento, eliminar_evento],
            system_instruction=(
                "ERES UN ASISTENTE DE CALENDARIO. IMPORTANTE: Los identificadores de los eventos "
                "son STRINGS (cadenas de texto) de Firebase como 'OZvDgeu...'. "
                "NUNCA digas que necesitas un número entero (int). Usa el ID de texto tal cual."
            )
            
        )
    )

    while True:
        user_input = input(f"\n{Fore.WHITE}Tu: ")
        if user_input.lower() in ['salir', 'exit', 'chao', 'bye']: 
            break

        try: 
            response = chat.send_message(user_input)
            print(f"{Fore.BLUE}IA: {Style.RESET_ALL}{response.text}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")