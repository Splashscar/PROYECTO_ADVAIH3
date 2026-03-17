from google import genai
client = genai.Client(api_key="AIzaSyD8C7e8aVOQ_6mbgwOv9sgygbmX1oaCJ1o")

for m in client.models.list():
    print(f"Modelo disponivle: {m.name}")