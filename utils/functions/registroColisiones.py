import pygame
import threading
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
from utils.functions.othersFunction import SacarUsuario

pygame.init()
def registroContinuo(usuario, id, pelota, fecha, bot, arco_derecho, arco_izquierdo):
    if usuario is None:
        return
    eventos = []
    if usuario.player_rect.colliderect(pelota.pelota_rect):
        x, y = usuario.player_rect.center
        eventos.append(("Pelota", x, y))
    if usuario.player_rect.colliderect(arco_izquierdo):
        x, y = usuario.player_rect.center
        eventos.append(("Gol", x, y))
    if usuario.player_rect.colliderect(bot.bot_hitbox):
        x, y = usuario.player_rect.center
        eventos.append(("Bot", x, y))
    if usuario.player_rect.colliderect(arco_derecho.rect):
        x, y = usuario.player_rect.center
        eventos.append(("ArcoDerecho", x, y))
    if usuario.player_rect.colliderect(arco_izquierdo.rect):
        x, y = usuario.player_rect.center
        eventos.append(("ArcoIzquierdo", x, y))

    for evento, x, y in eventos:
        with open("./utils/regist/registro.txt", "a", encoding="utf-8") as f:
            f.write(f"{id},{fecha},{evento},{x},{y}\n")
    return eventos

def evento_thread(id, eventos):
    def task():
        for evento, x, y in eventos:
            usuario = SacarUsuario(id)
            mensaje = generator(f"{usuario} chocó con el objeto {evento}", max_new_tokens=50)[0]["generated_text"]
            print(mensaje)
    threading.Thread(target=task, daemon=True).start()


from collections import defaultdict

def resumenCol():
    # 1. Leer usuarios y armar diccionario {id: nombre}
    usuarios = {}
    with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) >= 3:
                id_usuario = partes[0]
                nombre = partes[1]
                usuarios[id_usuario] = nombre

    # 2. Diccionario con la estructura de conteo
    resumen = defaultdict(lambda: {
        "Pelota": 0,
        "ArcoDerecho": 0,
        "ArcoIzquierdo": 0,
        "Bot": 0
    })

    # 3. Leer registros y acumular
    with open("./utils/regist/registro.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) < 3:
                continue
            id_usuario, _, tipo, *_ = partes

            if tipo in resumen[id_usuario]:
                resumen[id_usuario][tipo] += 1

    # 4. Guardar resumen cruzado con nombre
    with open("./utils/regist/resumen.txt", "w", encoding="utf-8") as f:
        for id_usuario, datos in resumen.items():
            nombre = usuarios.get(id_usuario, "Desconocido")
            f.write(f"{id_usuario},{nombre},{datos['Pelota']},{datos['ArcoDerecho']},{datos['ArcoIzquierdo']},{datos['Bot']}\n")

    print("✅ Resumen generado en ./utils/regist/resumen.txt")