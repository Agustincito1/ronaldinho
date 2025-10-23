import pygame
import threading
import logging
import os
from datetime import datetime

try:
    from config import (
        REGISTRO_SIZE, LONGITUD_PUNTERO_PRINCIPAL, RUTA_USUARIOS
    )
except ImportError:
    REGISTRO_SIZE = 41
    LONGITUD_PUNTERO_PRINCIPAL = 5
    RUTA_USUARIOS = "./utils/regist/usuarios.txt"
    OFFSET_A_PUNTERO_PRINCIPAL = 41

REGISTRO_EVENTO_SIZE = 57
LONGITUD_PUNTERO_EVENTO = 5
LONGITUD_EVENTO = 12
LONGITUD_ID_USUARIO = 4
RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"
OFFSET_A_REGSIG = 45

logging.getLogger("transformers").setLevel(logging.ERROR)
pygame.init()

def obtener_ultimo_registro_y_tamano():
    try:
        os.makedirs(os.path.dirname(RUTA_REGISTRO_EVENTOS), exist_ok=True)
        if not os.path.exists(RUTA_REGISTRO_EVENTOS):
            return 0, 0
        with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
            f.seek(0, 2)
            tamano_archivo = f.tell()
            ultimo_registro_numero = tamano_archivo // REGISTRO_EVENTO_SIZE 
            return tamano_archivo, ultimo_registro_numero
    except Exception as e:
        print(f"Error al obtener tamaño del registro: {e}")
        return 0, 0

def actualizar_puntero_siguiente(registro_a_actualizar, puntero_siguiente):
    offset_registro = (registro_a_actualizar - 1) * REGISTRO_EVENTO_SIZE
    offset_a_escribir = offset_registro + OFFSET_A_REGSIG
    nuevo_puntero_formateado = str(puntero_siguiente).zfill(LONGITUD_PUNTERO_EVENTO)
    try:
        with open(RUTA_REGISTRO_EVENTOS, "r+b") as f:
            f.seek(offset_a_escribir)
            f.write(nuevo_puntero_formateado.encode('utf-8'))
    except Exception as e:
        print(f"Error al actualizar puntero 'Siguiente' del registro {registro_a_actualizar}: {e}")

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
        tamano_total, num_registros_actuales = obtener_ultimo_registro_y_tamano()
        nuevo_registro_numero = num_registros_actuales + 1
        ultimo_registro_anterior = num_registros_actuales
        ultimo_registro_mismo_usuario = 0

        if num_registros_actuales > 0:
            with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
                for i in range(num_registros_actuales, 0, -1):
                    offset = (i - 1) * REGISTRO_EVENTO_SIZE
                    f.seek(offset + 6) 
                    id_reg = f.read(4).decode('utf-8')
                    if id_reg == str(id_usuario).zfill(LONGITUD_ID_USUARIO):
                        ultimo_registro_mismo_usuario = i
                        break

        if ultimo_registro_mismo_usuario > 0:
            reg_ant_puntero = str(ultimo_registro_mismo_usuario).zfill(LONGITUD_PUNTERO_EVENTO)  
        else:
            reg_ant_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
        
        reg_sig_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
        num_registro_formateado = str(nuevo_registro_numero).zfill(LONGITUD_PUNTERO_EVENTO)
        id_formateado = str(id_usuario).zfill(LONGITUD_ID_USUARIO)
        evento_formateado = evento.ljust(LONGITUD_EVENTO)[:LONGITUD_EVENTO]
        x_formateada = str(x).rjust(4)[:4]
        y_formateada = str(y).rjust(4)[:4]

        nuevo_registro_str = (
            f"{num_registro_formateado},"
            f"{id_formateado},"
            f"{fecha},"
            f"{evento_formateado},"
            f"{x_formateada},"
            f"{y_formateada},"
            f"{reg_sig_puntero},"
            f"{reg_ant_puntero}"
            f"\n"
        )
        
        nuevo_registro_bytes = nuevo_registro_str.encode('utf-8')
        
        if len(nuevo_registro_bytes) != REGISTRO_EVENTO_SIZE:
            print(f"ERROR CRÍTICO DE TAMAÑO: {len(nuevo_registro_bytes)} != {REGISTRO_EVENTO_SIZE}")
            continue

        try:
            with open(RUTA_REGISTRO_EVENTOS, "ab") as f:
                f.write(nuevo_registro_bytes)
                
            if ultimo_registro_mismo_usuario > 0:
                actualizar_puntero_siguiente(ultimo_registro_mismo_usuario, nuevo_registro_numero)

        except Exception as e:
            print(f"Error al registrar evento: {e}")

    return eventos
