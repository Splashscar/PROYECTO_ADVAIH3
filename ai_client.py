import time
import getpass
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import requests

# 1. Funcion de login

def login_usuario():
    print("--- login de usuario ---")
    email = input("Email: ")
    password = getpass.getpass("Contraseña: ")

    url_login = "http://127.0.0.1:8000/api/auth/login/"

    try:
        response = requests.post(
            url_login,
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            print("Usuario loggeado correctamente")
            return response.json().get("Token")

        print(f"Error: {response.json().get('error')}")

    except Exception as e:
        print("Error de conexion:", e)

    return None



# 2. Funcion de herramienta (Modificada para la IA)
def consultar_mis_tareas():
    """
    Consulta la lista de eventos o tareas del usuario autenticado en la API.
    No requiere argumentos.
    """
    # Usaremos la variable global 'token' que obtuvimos en el login
    global token 
    
    print("\n[SISTEMA]: La IA está consultando la API de eventos...")
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
    print(f"\n[SISTEMA]: La IA está ejecutando 'crear_nuevo_evento' para: {titulo}")
    
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
    

def actualizar_evento(id_evento: int, titulo: str = None, descripcion: str = None, fecha: str = None, lugar: str = None):
    """
    Actualiza los datos de un evento existente usando su ID.
    Solo envía los campos que el usuario quiera cambiar.
    """
    global token
    print(f"\n[SISTEMA]: Actualizando evento ID: {id_evento}...")
    
    url = f"http://127.0.0.1:8000/api/eventos/{id_evento}/"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Creamos un diccionario solo con los campos que no son None
    payload = {k: v for k, v in locals().items() if v is not None and k not in ['id_evento', 'headers', 'url']}

    try:
        res = requests.patch(url, json=payload, headers=headers) # Usamos PATCH para actualizar parcial
        if res.status_code == 200:
            return {"resultado": "Éxito", "detalle": "Evento actualizado correctamente"}
        else:
            return {"resultado": "Error", "detalle": res.json()}
    except Exception as e:
        return {"resultado": "Error de conexión", "detalle": str(e)}

# 3. Configuracion de la IA
load_dotenv(dotenv_path='proyecto_advaih/.env')

API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=API_KEY)

modelo_id = "gemini-2.5-flash"



# 4. Flujo de la lógica
token = login_usuario()

if token:
    print("IA: Hola, soy tu agente. ¿En qué puedo ayudarte hoy?")

    # IMPORTANTE: Definir el chat con el modo de "AUTOMATIC" para que 
    # la IA ejecute la función por sí sola.
    chat = client.chats.create(
        model=modelo_id,
        config=types.GenerateContentConfig(
            tools=[consultar_mis_tareas, crear_nuevo_evento]#,
            #automatic_function_calling=types.AutomaticFunctionCallingConfig(enabled=True)
        )
    )

    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ['salir', 'exit', 'chao', 'bye']: 
            break

        try: 
            # Enviamos el mensaje al chat
            response = chat.send_message(user_input)
            
            # Imprimimos la respuesta final (la IA ya habrá llamado a la función)
            print(f"IA: {response.text}")

        except Exception as e:
            print(f"Error: {e}")


