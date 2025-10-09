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


