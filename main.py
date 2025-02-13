from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Configuración del token de la API de DeepSeek
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Asegúrate de que esta URL sea válida
API_TOKEN = "sk-749a3ee548f64a078b82e56785966c07"  # Reemplaza con tu token real

# Inicializa la aplicación FastAPI
app = FastAPI()

# Modelo para la solicitud del usuario
class UserMessage(BaseModel):
    message: str

# Ruta principal del chatbot
@app.post("/chatbot/")
async def chatbot_endpoint(user_message: UserMessage):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    # Formato correcto de mensajes esperado por la API
    payload = {
        "model": "text-davinci-003",  # Ajusta el modelo según la documentación de DeepSeek si es necesario
        "messages": [
            {"role": "user", "content": user_message.message}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail=f"Error al comunicarse con DeepSeek: {e.response.text}")

    deepseek_response = response.json()
    return {
        "user_message": user_message.message,
        "bot_response": deepseek_response.get("choices", [{}])[0].get("message", {}).get("content", "No se recibió respuesta de DeepSeek."),
    }

# Ruta de prueba para verificar que la API está activa
@app.get("/")
async def root():
    return {"message": "El chatbot con FastAPI y DeepSeek está funcionando correctamente"}
