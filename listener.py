import os
from dotenv import load_dotenv
from google import genai

# 1. Cargamos el archivo .env donde está la llave de verdad
load_dotenv()

# 2. Obtenemos la llave desde la variable de entorno
API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Validamos que exista antes de crear el cliente
if not API_KEY:
    print("❌ ERROR: No se encontró la variable GEMINI_API_KEY en el archivo .env")
    exit()

client = genai.Client(api_key=API_KEY)

print("--- Verificando conexión con Gemini ---")
try:
    for m in client.models.list():
        print(f"Modelo disponible: {m.name}")
    print("\n✅ Conexión exitosa, la llave está funcionando.")
except Exception as e:
    print(f"❌ Error al conectar: {e}")