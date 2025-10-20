from collections import defaultdict
import os

# --- CONFIGURACIÓN DE LONGITUD FIJA PARA ARCHIVOS ---
# Nota: Asumimos que ID en usuarios.txt está con zfill(2)
LONGITUD_ID_RESUMEN = 2      # ID de usuario (e.g., '01')
LONGITUD_CONTADOR = 5        # Contador de eventos (e.g., '00042')
RUTA_USUARIOS = "./utils/regist/usuarios.txt"
RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"
RUTA_RESUMEN = "./utils/regist/resumen.txt"

# --- NUEVAS FUNCIONES DE ESTADÍSTICAS INDIVIDUALES ---

def sacar_usuario(user_id):
    """
    Función para extraer el nombre del usuario dado su ID.
    Asume que el ID es el primer campo y el Nombre el segundo en usuarios.txt.
    """
    usuario = "ID Desconocido"
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                # El registro de usuario es: ID, Nombre, Contraseña, Puntero
                partes = linea.strip().split(",")
                # El ID debe coincidir
                if len(partes) >= 1 and int(partes[0]) == int(user_id):
                    # El nombre está en la segunda parte (índice 1)
                    if len(partes) >= 2:
                        # Strip para limpiar los posibles espacios de relleno del nombre
                        usuario = partes[1].strip() 
                        return usuario
    except FileNotFoundError:
        print(f"Error: Archivo de usuarios no encontrado en {RUTA_USUARIOS}")
        return usuario
    return usuario

def estadisticas_usuario(user_id, anio=None):
    """
    Calcula estadísticas de juego (basadas en colisiones) para un usuario específico, 
    filtrando opcionalmente por año.
    """
    # Inicializamos contadores
    victorias = 0
    derrotas = 0
    empates = 0
    resumen_meses = [0]*12 

    try:
        with open(RUTA_REGISTRO_EVENTOS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                
                # Partes necesarias: ID, Fecha, Tipo de Evento
                if len(partes) < 3:
                    continue
                    
                # id_usuario está en partes[0], tipo está en partes[2] (debe limpiarse)
                id_usuario, fecha, tipo_raw = partes[:3]
                tipo = tipo_raw.strip().lower() # Limpiamos espacios y convertimos a minúsculas
                
                if int(id_usuario) != int(user_id):
                    continue
                    
                # Filtro por año (si se proporciona)
                if anio and not fecha.startswith(str(anio)):
                    continue

                # --- Mapeo de Colisión a Resultado de Partida ---
                # Esta es la lógica de conteo que proporcionaste:
                if tipo == "pelota":
                    victorias += 1
                elif tipo == "bot":
                    derrotas += 1
                elif tipo in ["arcoderecho", "arcoizquierdo"]: # Cubre los otros dos eventos
                    empates += 1

                # Resumen por mes
                # La fecha es YYYY-MM-DD (10 chars), el mes es el índice 1
                try:
                    mes = int(fecha.split("-")[1]) - 1  # Enero=0
                    if 0 <= mes < 12:
                         resumen_meses[mes] += 1
                except (ValueError, IndexError):
                    # Manejar formatos de fecha inválidos si es necesario
                    pass 

    except FileNotFoundError:
        print(f"Error: Archivo de registro no encontrado en {RUTA_REGISTRO_EVENTOS}")
        
    total_partidas = victorias + derrotas + empates
    nombre = sacar_usuario(user_id) # Llamada a la nueva función

    return {
        "nombre": nombre,
        "totalPartidas": total_partidas,
        "victorias": victorias,
        "derrotas": derrotas,
        "empates": empates,
        "resumenMeses": resumen_meses
    }


# --- FUNCIÓN DE RESUMEN GLOBAL (Mantenida) ---

def resumenCol():
    """
    Lee todos los registros de eventos, cuenta las colisiones por tipo 
    para cada ID de usuario y escribe el resumen en un archivo de longitud fija, 
    SIN incluir el nombre del usuario.
    Formato de salida fijo: ID(2),Pelota(5),ArcoDerecho(5),ArcoIzquierdo(5),Bot(5)\n (27 bytes)
    """
    
    # 1. Leer usuarios para obtener solo los IDs válidos
    # Esto asegura que solo procesemos IDs que existen en el sistema.
    usuarios_ids = set()
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                # El ID es el primer campo del registro de 48 bytes
                partes = linea.strip().split(",")
                if len(partes) >= 1 and partes[0]:
                    # Aseguramos que el ID siempre sea de 2 caracteres
                    usuarios_ids.add(partes[0].zfill(LONGITUD_ID_RESUMEN)) 
    except FileNotFoundError:
        print(f"⚠️ Archivo de usuarios no encontrado en {RUTA_USUARIOS}. No se puede generar el resumen.")
        return

    # 2. Diccionario con la estructura de conteo inicializado a cero para cada ID
    resumen = defaultdict(lambda: {
        "Pelota": 0,
        "ArcoDerecho": 0,
        "ArcoIzquierdo": 0,
        "Bot": 0
    })

    # 3. Leer registros de eventos (registro.txt) y acumular
    try:
        with open(RUTA_REGISTRO_EVENTOS, "r", encoding="utf-8") as f:
            for linea in f:
                # El archivo de registro de eventos es de 50 bytes de longitud fija.
                # Usamos split para extraer las partes.
                partes = linea.strip().split(",") 
                
                # Necesitamos al menos 3 partes (ID, Fecha, TipoEvento)
                if len(partes) < 3:
                    continue
                    
                id_usuario = partes[0].zfill(LONGITUD_ID_RESUMEN)
                
                # El tipo de evento (partes[2]) está relleno con espacios (ljust(12)), 
                # por eso usamos .strip() para obtener el nombre exacto del evento.
                tipo_evento = partes[2].strip() 
                
                # Solo contamos si el ID es conocido y el tipo de evento es relevante
                if id_usuario in usuarios_ids and tipo_evento in resumen[id_usuario]:
                    resumen[id_usuario][tipo_evento] += 1
    
    except FileNotFoundError:
        print(f"⚠️ Archivo de registro de eventos no encontrado en {RUTA_REGISTRO_EVENTOS}. El resumen estará vacío.")

    # 4. Guardar resumen en formato de LONGITUD FIJA (27 bytes por línea)
    try:
        with open(RUTA_RESUMEN, "w", encoding="utf-8") as f:
            # Ordenamos los IDs para una mejor legibilidad del archivo final
            for id_usuario in sorted(list(usuarios_ids)):
                # Obtener los datos, usando defaultdict para IDs sin eventos
                datos = resumen[id_usuario]
                
                # Aplicar ZFILL para obtener los 5 bytes de longitud fija para cada contador
                pelota = str(datos['Pelota']).zfill(LONGITUD_CONTADOR)
                arco_derecho = str(datos['ArcoDerecho']).zfill(LONGITUD_CONTADOR)
                arco_izquierdo = str(datos['ArcoIzquierdo']).zfill(LONGITUD_CONTADOR)
                bot = str(datos['Bot']).zfill(LONGITUD_CONTADOR)
                
                # Escribir el registro de longitud fija (27 bytes)
                f.write(
                    f"{id_usuario},"      # 2 bytes
                    f"{pelota},"          # 5 bytes
                    f"{arco_derecho},"    # 5 bytes
                    f"{arco_izquierdo},"  # 5 bytes
                    f"{bot}\n"            # 5 bytes + \n
                )

        print(f"✅ Resumen de colisiones generado en {RUTA_RESUMEN}. (Formato fijo: ID(2),Contador(5)x4)")
    except Exception as e:
        print(f"❌ Error al escribir el archivo resumen: {e}")
