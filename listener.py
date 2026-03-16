from google import genai
client = genai.Client(api_key="AIzaSyDoehzPkT0UaA8_8OuZZHtpt1WGNw2DaDc")

for m in client.models.list():
    print(f"Modelo disponivle: {m.name}")