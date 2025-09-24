from transformers import pipeline

# Pipeline de texto con PyTorch
generator = pipeline(
    "text-generation",
    model="EleutherAI/gpt-neo-1.3B",
    device=-1,       # CPU
    framework="pt"   # fuerza PyTorch
)

prompt = "Agustín choca con la pelota. Escribe un mensaje divertido, breve y coherente celebrando la colisión."



# Generar mensaje
resultado = generator(
    prompt,
    max_new_tokens=15,   # mensaje corto
    do_sample=True,
    temperature=0.5,     # creatividad
    return_full_text=False
)

# Solo la respuesta, sin repetir el prompt
mensaje = resultado[0]['generated_text'].strip()

print(mensaje)
