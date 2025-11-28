import pygame
from datetime import datetime
import logging
import os
from utils.puntero.punteroObj import PunteroObj

registrador = PunteroObj()

def registroContinuo(usuario, id_usuario, pelota, fecha, bot, arco_derecho, arco_izquierdo):

    if usuario is None:
        return []
    
    eventos = []

    if usuario.rect.colliderect(pelota.pelota_rect):
        x, y = usuario.rect.center
        eventos.append(("Pelota", x, y))
    if usuario.rect.colliderect(bot.hitbox):
        x, y = usuario.rect.center
        eventos.append(("Bot", x, y))
    if usuario.rect.colliderect(arco_derecho.goal_area_rect):
        x, y = usuario.rect.center
        eventos.append(("ArcoDerecho", x, y))
    if usuario.rect.colliderect(arco_izquierdo.goal_area_rect):
        x, y = usuario.rect.center
        eventos.append(("ArcoIzquierdo", x, y))


    for evento, x, y in eventos:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if x is None or y is None:
            x, y = 0, 0
            
        registrador.registrarEvento(id_usuario, fecha, evento, x, y)
        
    return eventos



def registrar_resultado(id_usuario, resultado):
    #N EMPATE W GANA L PIERDE
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use the result-specific registrar on the PunteroObj
    registrador.registrarResultado(id_usuario, fecha, resultado)



