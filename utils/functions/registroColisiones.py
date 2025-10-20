import pygame
import threading
import logging
import os 
from datetime import datetime
# Importamos las constantes necesarias. Asumimos que estas están definidas en config.py
# o en tu archivo principal, con los valores de 48 y 5.
try:
    from config import (
        REGISTRO_SIZE, LONGITUD_PUNTERO_PRINCIPAL, RUTA_USUARIOS
    )
except ImportError:
    # Definiciones de constantes por si no tienes el archivo config.py accesible aquí
    # ASUMIMOS estas constantes de la conversación anterior:
    REGISTRO_SIZE = 48
    LONGITUD_PUNTERO_PRINCIPAL = 5
    RUTA_USUARIOS = "./utils/regist/usuarios.txt"
    # El puntero empieza en el byte 41 del registro de 48 bytes:
    OFFSET_A_PUNTERO_PRINCIPAL = 41 

logging.getLogger("transformers").setLevel(logging.ERROR)
# from utils.functions.othersFunction import SacarUsuario # Asumido
pygame.init()

# --- CONFIGURACIÓN DE REGISTRO DE EVENTOS (Mantenidas) ---
REGISTRO_EVENTO_SIZE = 50 
LONGITUD_PUNTERO_EVENTO = 5 
LONGITUD_EVENTO = 12 
RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"

# La siguiente ruta ya NO se usa
# RUTA_USUARIOS_INDEX = "./utils/regist/usuarios_index.txt" 

# --- FUNCIONES DE CÁLCULO DE REGISTROS DE EVENTOS (Mantenidas) ---

def obtener_ultimo_registro_y_tamano():
    """Calcula el tamaño del archivo y el número del último registro escrito."""
    # ... (Lógica de cálculo de tamaño de registro.txt se mantiene) ...
    try:
        if not os.path.exists(RUTA_REGISTRO_EVENTOS):
            return 0, 0
            
        with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
            f.seek(0, 2)
            tamano_archivo = f.tell()
            # Usamos REGISTRO_EVENTO_SIZE = 50
            ultimo_registro_numero = tamano_archivo // REGISTRO_EVENTO_SIZE 
            return tamano_archivo, ultimo_registro_numero
    except Exception:
        return 0, 0

# --------------------------------------------------------------------------
# --- FUNCIONES CLAVE MODIFICADAS: USAN RUTA_USUARIOS EN LUGAR DEL ÍNDICE ---
# --------------------------------------------------------------------------

def leer_ultimo_puntero_usuario(id_usuario):
    """
    Lee el puntero al último evento (RegUltimoEvento) desde el registro 
    principal del usuario (RUTA_USUARIOS) usando SEEK.
    """
    try:
        # Abrimos en modo de lectura binaria ('rb')
        with open(RUTA_USUARIOS, "rb") as f:
            # El ID es el número de registro (1, 2, 3...)
            offset_registro = (id_usuario - 1) * REGISTRO_SIZE # 48 bytes
            
            # El puntero comienza después de ID(2), Nombre(18), Contraseña(18) = 2+1+18+1+18+1 = 41 bytes
            # Usamos la constante o variable definida:
            OFFSET_A_PUNTERO_PRINCIPAL = 41 # Ajustar si el REGISTRO_SIZE no es 48
            
            # Posición exacta de inicio del puntero de 5 bytes
            f.seek(offset_registro + OFFSET_A_PUNTERO_PRINCIPAL)
            
            # Leer exactamente los 5 bytes del puntero
            puntero_bytes = f.read(LONGITUD_PUNTERO_PRINCIPAL)
            
            # Si no se lee la longitud esperada, algo salió mal
            if len(puntero_bytes) != LONGITUD_PUNTERO_PRINCIPAL:
                return 0
                
            # Decodificamos y convertimos a entero
            return int(puntero_bytes.decode('utf-8').strip())
            
    except Exception:
        return 0

def actualizar_ultimo_puntero_usuario(id_usuario, nuevo_puntero):
    """
    Actualiza el puntero al último evento en el registro principal (RUTA_USUARIOS) 
    usando SEEK y 'r+b'.
    """
    
    offset_registro = (id_usuario - 1) * REGISTRO_SIZE # 48 bytes
    OFFSET_A_PUNTERO_PRINCIPAL = 41
    offset_a_escribir = offset_registro + OFFSET_A_PUNTERO_PRINCIPAL
    
    # El nuevo puntero debe tener 5 caracteres, rellenado con ceros (e.g., '00037')
    nuevo_puntero_formateado = str(nuevo_puntero).zfill(LONGITUD_PUNTERO_PRINCIPAL)
    
    try:
        # Abrir en modo de lectura y escritura binaria ('r+b')
        with open(RUTA_USUARIOS, "r+b") as f:
            
            # Mover el puntero a la posición exacta
            f.seek(offset_a_escribir)
            
            # Escribir los 5 bytes del nuevo puntero
            f.write(nuevo_puntero_formateado.encode('utf-8'))
            
    except Exception as e:
        print(f"Error al actualizar puntero principal del usuario {id_usuario}: {e}")

# --------------------------------------------------------------------------
# --- FUNCIÓN PRINCIPAL DE REGISTRO (registroContinuo) ---
# --------------------------------------------------------------------------

def registroContinuo(usuario, id_usuario, pelota, fecha, bot, arco_derecho, arco_izquierdo):
    if usuario is None:
        return []
    
    eventos = []
    
    # --- Detección de Colisiones (Mantenida) ---
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


    # --- IMPLEMENTACIÓN DE DOBLE ENLACE ---

    for evento, x, y in eventos:
        # 1. Obtener la posición (número) del registro anterior
        # AHORA lee directamente del registro principal (RUTA_USUARIOS)
        ultimo_registro_anterior = leer_ultimo_puntero_usuario(id_usuario)
        
        # 2. Calcular número y posición del NUEVO registro
        tamano_total, num_registros_actuales = obtener_ultimo_registro_y_tamano()
        nuevo_registro_numero = num_registros_actuales + 1
        
        # El puntero "Anterior" (RegAnt) del nuevo registro es el número del último evento
        reg_ant_puntero = str(ultimo_registro_anterior).zfill(LONGITUD_PUNTERO_EVENTO)
        
        # El puntero "Siguiente" (RegSig) siempre es 0 al escribirse por primera vez
        reg_sig_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO) 

        # 3. Formatear y Escribir el Nuevo Registro (Modo 'a' en registro.txt)
        
        id_formateado = str(id_usuario).zfill(2)
        evento_formateado = evento.ljust(LONGITUD_EVENTO)
        x_formateada = str(x).ljust(4)
        y_formateada = str(y).ljust(4)
        
        nuevo_registro = (
            f"{id_formateado},"
            f"{fecha}," # Asumimos 'fecha' es YYYY-MM-DD (10 chars)
            f"{evento_formateado},"
            f"{x_formateada},"
            f"{y_formateada},"
            f"{reg_sig_puntero}," # Inicialmente 0
            f"{reg_ant_puntero}\n"
        )

        try:
            # Escribir el nuevo registro al final de registro.txt
            with open(RUTA_REGISTRO_EVENTOS, "a", encoding="utf-8") as f:
                f.write(nuevo_registro)
            
            # 4. Actualizar el puntero 'Siguiente' del registro ANTERIOR (en registro.txt)
            if ultimo_registro_anterior > 0:
                actualizar_puntero_siguiente(ultimo_registro_anterior, nuevo_registro_numero)

            # 5. Actualizar el puntero 'Último Evento' en el registro principal (en usuarios.txt)
            actualizar_ultimo_puntero_usuario(id_usuario, nuevo_registro_numero)

        except Exception as e:
            print(f"Error al registrar evento: {e}")

    return eventos

# --------------------------------------------------------------------------
# --- FUNCIÓN CLAVE: ACTUALIZAR PUNTERO SIGUIENTE EN REGISTRO DE EVENTOS (Mantenida) ---
# --------------------------------------------------------------------------

def actualizar_puntero_siguiente(registro_a_actualizar, puntero_siguiente):
    """
    Usa seek() para ir al registro de evento anterior y actualizar 
    SOLO el campo RegSig (el puntero 'Siguiente').
    """
    
    # 1. Calcular el OFFSET (posición de inicio del registro anterior)
    offset_registro = (registro_a_actualizar - 1) * REGISTRO_EVENTO_SIZE # 50 bytes
    
    # 2. Calcular el OFFSET del campo RegSig dentro del registro de 50 bytes
    # ID(2)+,+(1) + Fecha(10)+,+(1) + Evento(12)+,+(1) + X(4)+,+(1) + Y(4)+,+(1) = 37 bytes
    OFFSET_A_REGSIG = 37 
    offset_a_escribir = offset_registro + OFFSET_A_REGSIG
    
    # 3. Formatear el nuevo puntero (5 bytes)
    nuevo_puntero_formateado = str(puntero_siguiente).zfill(LONGITUD_PUNTERO_EVENTO)
    
    try:
        # Abrir en modo de lectura y escritura binaria ('r+b')
        with open(RUTA_REGISTRO_EVENTOS, "r+b") as f:
            f.seek(offset_a_escribir)
            f.write(nuevo_puntero_formateado.encode('utf-8'))
            
    except Exception as e:
        print(f"Error al actualizar puntero 'Siguiente' del registro {registro_a_actualizar}: {e}")