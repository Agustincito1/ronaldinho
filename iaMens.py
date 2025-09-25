from transformers import pipeline

# Pipeline de texto con PyTorch
generator = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-1.3B",
    device=-1,       # CPU
    framework="pt"   # fuerza PyTorch
)

async def generar_mensaje(usuario, evento):
    prompt = f"{usuario}, choco con {evento}. dame un mensaje describiendo el evento de forma divertida y breve."

    # Generar mensaje
    resultado = generator(
        prompt,
        max_new_tokens=25,   # mensaje corto
        do_sample=True,
        temperature=0.5,     # creatividad
        return_full_text=False
    )
    
    # Solo la respuesta, sin repetir el prompt
    mensaje = resultado[0]['generated_text'].strip()
    print(mensaje)
    return mensaje
