import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
print("Usando chave:", api_key[:10] + "...")

client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-2.5-flash")

resposta = chat.send_message("Diga 'olá mundo'")
print(resposta.text)
