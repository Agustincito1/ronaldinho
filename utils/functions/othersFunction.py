import random
import pygame
from config import FPS, clock
def SacarUsuario(id):
    # Leer usuarios
    usuario = ""
    with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if int(partes[0]) == int(id):
                if len(partes) >= 2:
                    usuario = partes[1]
    return usuario


def leerRegistros(id):
    registros = []
    with open("./utils/regist/registro.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if int(partes[0]) == int(id):
                user_id, fecha, objeto, x, y = partes
                if user_id.isdigit():
                    registros.append({
                        "user_id": user_id,
                        "fecha": fecha,
                        "objeto": objeto,
                        "x": int(x),
                        "y": int(y)
                    })

    return registros


def fisicas(jugador, bot, pelota, keys):
    
    # 1. Colisión Personaje vs. Personaje (Separación Mutua)
    if jugador.hitbox.colliderect(bot.hitbox):
        empuje = 5
        if jugador.rect.centerx < bot.rect.centerx:
            jugador.rect.x -= empuje
            bot.rect.x += empuje
        else:
            jugador.rect.x += empuje
            bot.rect.x -= empuje
            
    # 2. Colisión Jugador vs. Pelota (Evitar Traspaso - Mueve al JUGADOR)
    if jugador.hitbox.colliderect(pelota.pelota_rect):
        dx = (jugador.hitbox.centerx - pelota.pelota_rect.centerx)
        min_dist = jugador.hitbox.width / 2 + pelota.pelota_rect.width / 2
        
        if abs(dx) < min_dist:
            overlap = min_dist - abs(dx)
            
            if dx > 0:
                jugador.rect.x += overlap
            else:
                jugador.rect.x -= overlap
            
    # 3. Colisión Bot vs. Pelota (Evitar Traspaso - Mueve al BOT)
    if bot.hitbox.colliderect(pelota.pelota_rect):
        dx = (bot.hitbox.centerx - pelota.pelota_rect.centerx)
        min_dist = bot.hitbox.width / 2 + pelota.pelota_rect.width / 2
        
        if abs(dx) < min_dist:
            overlap = min_dist - abs(dx)
            
            if dx > 0:
                bot.rect.x += overlap
            else:
                bot.rect.x -= overlap

    # 4. Colisión y manejo de impacto de la Pelota (Aplica la velocidad a la pelota)
    colision_con_jugador = pelota.check_colision(jugador, "jugador")
    if colision_con_jugador == "jugador":
        es_patada = keys[pygame.K_SPACE]
        pelota.manejar_impacto(jugador, es_patada)
        
    colision_con_bot = pelota.check_colision(bot, "bot") 
    if colision_con_bot == "bot":
        pelota.manejar_impacto(bot, es_patada=True)
