import openai
import os


openai.api_key = "DRNY_MbPrGlC6EIdQfi8njlZyl2ui5V3jgsOrSiWFX4"

openai.api_base = "https://api.poe.com/v1"

async def generar_mensaje(usuario, evento):
    prompt = f"{usuario}, chocó con {evento}. Dame un mensaje divertido y breve. si dice GOL fue porque hizo un gol. entonces no es una colisión, es un gol. no digas nada de colisiones en ese caso. solo el mensaje divertido."

    chat = openai.ChatCompletion.create(
        model="BotLX18X5TJQ9", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=30,
        temperature=0.7
    )

    mensaje = chat.choices[0].message["content"].strip()
    print(mensaje)
    return mensaje


##bot con preguntas y respuestas interacion entre los do, la ia te puntua se registra la bd

#respuesta en txt

#Empresa te responde con una nueva recompensa
#EDucacion del ambiente

#Mercado de puntos, 

#El juego se puede mantener con anuncios? 
#El juego debe generar algo para la empresa gane

#No se si es tan factible

#
