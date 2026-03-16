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


