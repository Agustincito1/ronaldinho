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
    
    # 1. Colisión con la pelota
    if usuario.rect.colliderect(pelota.pelota_rect):
        x, y = usuario.rect.center
        eventos.append(("Pelota", x, y))
        
    # 2. Colisión con el Bot
    if usuario.rect.colliderect(bot.hitbox):
        x, y = usuario.rect.center
        eventos.append(("Bot", x, y))
        
    # 3. Colisión con Arco Derecho (usando el rectángulo del área de gol)
    if usuario.rect.colliderect(arco_derecho.goal_area_rect):
        x, y = usuario.rect.center
        eventos.append(("ArcoDerecho", x, y))
        
    # 4. Colisión con Arco Izquierdo (usando el rectángulo del área de gol)
    if usuario.rect.colliderect(arco_izquierdo.goal_area_rect):
        x, y = usuario.rect.center
        eventos.append(("ArcoIzquierdo", x, y))

    for evento, x, y in eventos:
        with open("./utils/regist/registro.txt", "a", encoding="utf-8") as f:
            f.write(f"{id},{fecha},{evento},{x},{y}\n")
    return eventos

