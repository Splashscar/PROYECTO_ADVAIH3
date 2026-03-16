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
