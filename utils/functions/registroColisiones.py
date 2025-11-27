import pygame
from datetime import datetime
import logging
import os
# --- 1. Inicialización de la clase de gestión de archivos ---
# Crea una instancia global para gestionar los archivos de eventos.


def registroContinuo(gestor_eventos, usuario, id_usuario, pelota, fecha, bot, arco_derecho, arco_izquierdo):

    if usuario is None:
        return []
    
    eventos = []
    
    # 1. Detección de eventos (se mantiene la lógica original de Pygame)
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
        
    # 2. Procesamiento y registro
    for evento, x, y in eventos:
        
        # A. Obtener el ID del último registro de evento insertado para este usuario.
        # Usa el nuevo método findLastEventIdForUser (reemplaza selectFilaUsuario)
        ultimo_registro_mismo_usuario = gestor_eventos.findLastEventIdForUser(id_usuario)

        # B. Insertar el nuevo evento en el archivo enlazado (registro.txt)
        nuevo_id_reg = gestor_eventos.insertEvent(
            id_usuario, datetime.now().strftime("%Y-%m-%d"), evento, x, y, ultimo_registro_mismo_usuario
        )
        
        if nuevo_id_reg is None:
            continue # Falló la inserción
            
        # C. Actualizar punteros

        if ultimo_registro_mismo_usuario > 0:
            gestor_eventos.updatePointer(ultimo_registro_mismo_usuario, nuevo_id_reg)
    return eventos





# --- CONSTANTES DE CONFIGURACIÓN ---
# Las constantes de configuración necesarias están definidas aquí, ya que este
# módulo es independiente de la estructura de eventos de 'objectPuntero.py'.

# Tamaño total de un registro de resultado (5+4+10+1+5+5 + 5 comas + \n) = 36
REGISTRO_EVENTO_SIZE = 36 
LONGITUD_PUNTERO_EVENTO = 5  # Para IdReg, sig y ant
LONGITUD_ID_USUARIO = 4      # Para IdUser
LONGITUD_RESULTADO = 1       # Para el campo 'resultado' (W, L, N)

RUTA_REGISTRO_EVENTOS = "./utils/regist/resultados.txt"

# Offset para el puntero "sig" (siguiente):
# IdReg(5) + ,(1) + IdUser(4) + ,(1) + Fecha(10) + ,(1) + Resultado(1) + ,(1) = 24
OFFSET_A_REGSIG = 24 

# --- FUNCIONES DE UTILIDAD ---

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
        # Abrir en modo de lectura/escritura binaria
        with open(RUTA_REGISTRO_EVENTOS, "r+b") as f:
            f.seek(offset_a_escribir)
            f.write(nuevo_puntero_formateado.encode('utf-8'))
    except Exception as e:
        print(f"Error al actualizar puntero 'Siguiente' del registro {registro_a_actualizar}: {e}")

def registrar_resultado(id_usuario, resultado):

    if id_usuario is None:
        return 

    fecha = datetime.now().strftime("%Y-%m-%d")
    # Normalizar el resultado (W, L, N)
    resultado_norm = (resultado[0].upper() if resultado and resultado[0].upper() in ('W', 'L', 'N') else "N") 
    
    tamano_total, num_registros_actuales = obtener_ultimo_registro_y_tamano()
    nuevo_registro_numero = num_registros_actuales + 1
    ultimo_registro_mismo_usuario = 0
    

    # 1. Buscar el último registro de este usuario
    if num_registros_actuales > 0:
        # Offset para IdUser: IdReg(5) + ,(1) = 6
        OFFSET_A_IDUSER = 6 
        id_user_formateado = str(id_usuario).zfill(LONGITUD_ID_USUARIO)
        
        with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
            # Iterar hacia atrás (desde el último registro)
            for i in range(num_registros_actuales, 0, -1):
                offset = (i - 1) * REGISTRO_EVENTO_SIZE
                f.seek(offset + OFFSET_A_IDUSER) 
                
                # Leer el ID del usuario
                id_reg = f.read(LONGITUD_ID_USUARIO).decode('utf-8')
                
                if id_reg == id_user_formateado:
                    ultimo_registro_mismo_usuario = i
                    break

    # 2. Configurar punteros para el nuevo registro
    if ultimo_registro_mismo_usuario > 0:
        # El puntero anterior es el último registro encontrado
        reg_ant_puntero = str(ultimo_registro_mismo_usuario).zfill(LONGITUD_PUNTERO_EVENTO) 
    else:
        # Primer registro para este usuario
        reg_ant_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
        
    # El puntero siguiente del nuevo registro siempre es 0
    reg_sig_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
    num_registro_formateado = str(nuevo_registro_numero).zfill(LONGITUD_PUNTERO_EVENTO)
    id_formateado = str(id_usuario).zfill(LONGITUD_ID_USUARIO)

    # 3. Construir la cadena de registro
    nuevo_registro_str = (
        num_registro_formateado + "," + 
        id_formateado + "," +
        fecha + "," +
        resultado_norm + "," +
        reg_sig_puntero + "," +
        reg_ant_puntero +
        "\n"
    )
    
    nuevo_registro_bytes = nuevo_registro_str.encode('utf-8')
        
    # 4. Validación de longitud y escritura
    if len(nuevo_registro_bytes) != REGISTRO_EVENTO_SIZE:
        print(f"ERROR CRÍTICO DE TAMAÑO: {len(nuevo_registro_bytes)} != {REGISTRO_EVENTO_SIZE}")
        print(f"  Registro creado (repr): {repr(nuevo_registro_str)}")
        return


    try:
        # Escribir el nuevo registro
        with open(RUTA_REGISTRO_EVENTOS, "ab") as f:
            f.write(nuevo_registro_bytes)
            
        # 5. Actualizar el puntero del registro anterior si existe
        if ultimo_registro_mismo_usuario > 0:
            actualizar_puntero_siguiente(ultimo_registro_mismo_usuario, nuevo_registro_numero)

    except Exception as e:
        print(f"Error al registrar evento: {e}")

    return