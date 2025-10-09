import openai
import os

# Tomar la API key de la variable de entorno
openai.api_key = os.getenv("POE_API_KEY")
openai.api_base = "https://api.poe.com/v1"

async def generar_mensaje(usuario, evento):
    prompt = f"{usuario}, chocó con {evento}. Dame un mensaje divertido y breve. si dice GOL fue porque hizo un gol. entonces no es una colisión, es un gol. no digas nada de colisiones en ese caso. solo el mensaje divertido."

    chat = openai.ChatCompletion.create(
        model="BotLX18X5TJQ9",  # reemplazá con tu bot de Poe
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30,
        temperature=0.7
    )

    mensaje = chat.choices[0].message["content"].strip()
    print(mensaje)
    return mensaje
