import time
import getpass
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
            return response.json().get("token")

        print(f"Error: {response.json().get('error')}")

    except Exception as e:
        print("Error de conexion:", e)

    return None


# 2. Herramienta que la IA puede usar

def consultar_mis_tareas(token_firebase):
    """
    Consulta la lista de tareas del usuario autenticado en la API
    """

    print("EL SISTEMA ESTA CONSULTANDO LA API")

    url = "http://127.0.0.1:8000/api/tareas/"

    headers = {
        "Authorization": f"Bearer {token_firebase}"
    }

    print(f"Enviando cabeceras: {headers}")

    try:
        res = requests.get(url, headers=headers)
        return res.json()

    except Exception as e:
        return {"error": str(e)}


# 3. Configuracion de la IA

API_KEY = "AIzaSyDoehzPkT0UaA8_8OuZZHtpt1WGNw2DaDc"

client = genai.Client(api_key=API_KEY)

modelo_id = "gemini-2.5-flash"


# 4. Flujo de la logica

token = login_usuario()

if token:

    print("IA: Hola soy tu agente de IA integrado a la API")

    while True:

        user_input = input("\nTu: ")

        if user_input.lower() in ["salir", "exit", "chao", "bye"]:
            break

        prompt = (
            f"Contexto de seguridad: El token es {token}. "
            f"Usuario pregunta: {user_input}. "
            f"Usa la herramienta 'consultar_mis_tareas' si el usuario pregunta por sus tareas."
        )

        try:

            response = client.models.generate_content(
                model=modelo_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[consultar_mis_tareas]
                )
            )

            print(f"IA: {response.text}")

        except Exception as e:

            error_str = str(e)

            if "429" in error_str:
                print("IA: Agotamos las peticiones gratuitas del minuto, espera 20 segundos")
                time.sleep(20)

            elif "404" in error_str:
                print("IA: Error en la version del modelo")

            else:
                print("Error de conexion:", e)