import os 
from datetime import datetime

# --- CONFIGURACIÓN DE ESTRUCTURAS DE ARCHIVO ---

# Estructura del Archivo de Eventos (registro.txt)
# Longitud Total: 57 bytes (5+4+10+12+4+4+5+5 + 7 comas + \n)
COLUMNAS_EVENTOS = {
    "IdReg": 5,           # Número de registro secuencial (Puntero/ID)
    "IdUser": 4,          # ID del usuario (clave de enlace)
    "Fecha": 10,          # YYYY-MM-DD
    "Evento": 12,         # Tipo de evento (ArcoDerecho, Pelota, etc.)
    "X": 4,               # Coordenada X
    "Y": 4,               # Coordenada Y
    "sig": 5,             # Puntero Siguiente (Next)
    "ant": 5              # Puntero Anterior (Prev/Preview)
}
RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"
LONGITUD_ID_USUARIO = 4 # Para formatear el ID de usuario

# --- FUNCIONES DE UTILIDAD ---

# Función unificada para rellenar
def rellenar(text, ancho, tipo="derecha_espacio"):
    text = str(text)
    if len(text) > ancho:
        return text[:ancho]
    
    if tipo == "izquierda":
        return text.zfill(ancho)
    elif tipo == "derecha_espacio":
        return text.ljust(ancho)
    else: # Por defecto: derecha con espacio
        return text.ljust(ancho)

# --- CLASE PRINCIPAL ArchivoEventos ---

class ArchivoEventos:

    def __init__(self, columnas_estructura, ruta_archivo): # Eliminado: usuario_cols, usuario_ruta
        self.columnas = columnas_estructura
        self.ruta_archivo = ruta_archivo
        self.max_fila = self._calcularMax(self.columnas)
        self.longitud_puntero = columnas_estructura["sig"] 
        self.offsets = self._calcularOffsets()

    def _calcularMax(self, columnas):
        # Calcula la longitud total de una fila (registro) en bytes/caracteres
        num_columnas = len(columnas)
        suma_anchos = sum(columnas.values())
        num_separadores = num_columnas - 1
        return suma_anchos + num_separadores + 1

    def _calcularOffsets(self):
        # Calcula los offsets cruciales para el archivo de eventos (registro.txt)
        offsets = {}
        
        # Offset para el puntero Siguiente (sig) en registro.txt
        # 5(IdReg)+1(,) + 4(IdUser)+1(,) + 10(Fecha)+1(,) + 12(Evento)+1(,) + 4(X)+1(,) + 4(Y)+1(,) = 45
        offset_sig = sum(self.columnas[key] + 1 for key in ["IdReg", "IdUser", "Fecha", "Evento", "X", "Y"])
        offsets['sig'] = offset_sig - 1 # Posición de inicio del campo 'sig'
        
        # Offset para la columna IdUser (5(IdReg) + 1(,)= 6)
        offsets['IdUser'] = self.columnas["IdReg"] + 1 
        
        return offsets

    def getNewID(self):
        # Obtiene el nuevo ID basado en el tamaño del archivo de eventos
        file_path = self.ruta_archivo
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return 1 

        try:
            with open(file_path, "rb") as f:
                cantidad_bytes = f.seek(0, 2)
                if self.max_fila > 0:
                    return (cantidad_bytes // self.max_fila) + 1
                return 1
        except Exception as e:
            print(f"Error al obtener nuevo ID: {e}")
            return 1
    
    def findLastEventIdForUser(self, id_usuario):
        file_path = self.ruta_archivo
        id_formateado = rellenar(id_usuario, LONGITUD_ID_USUARIO, tipo="izquierda")
        try:
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return 0
                
            with open(file_path, "rb") as f:
                tamano_total = f.seek(0, 2)
                num_registros_actuales = tamano_total // self.max_fila
                
                for i in range(num_registros_actuales, 0, -1):
                    offset_registro = (i - 1) * self.max_fila
                    offset_a_leer_id_user = offset_registro + self.offsets['IdUser']
                    
                    # Leer el IdUser (4 bytes)
                    f.seek(offset_a_leer_id_user) 
                    id_reg = f.read(LONGITUD_ID_USUARIO).decode('utf-8')
                    
                    if id_reg == id_formateado:
                        return i # Retorna el ID de registro del último evento encontrado
            
            return 0 # No se encontró ningún registro para el usuario
            
        except Exception as e:
            print(f"Error al buscar el último registro del usuario {id_usuario}: {e}")
            return 0 

    def updatePointer(self, registro_a_actualizar, puntero_siguiente):
        """Actualiza el puntero 'sig' de un registro enlazado con el ID del nuevo registro."""
        
        offset_registro = (registro_a_actualizar - 1) * self.max_fila
        offset_a_escribir = offset_registro + self.offsets['sig']
        
        # Formateo del puntero a 5 caracteres con ceros a la izquierda
        nuevo_puntero_formateado = rellenar(puntero_siguiente, self.longitud_puntero, tipo="izquierda")
        
        try:
            with open(self.ruta_archivo, "r+b") as f:
                f.seek(offset_a_escribir+1)
                f.write(nuevo_puntero_formateado.encode('utf-8'))
        except Exception as e:
            print(f"Error al actualizar puntero 'sig' del registro {registro_a_actualizar}: {e}")
            
    def insertEvent(self, id_usuario, fecha, evento, x, y, ultimo_reg_usuario):
        """Inserta un nuevo registro de evento con los punteros 'sig' y 'ant' establecidos."""
        
        nuevo_id_reg = self.getNewID()
        
        # 1. Determinar punteros del nuevo registro
        # 'ant' es el último_reg_usuario encontrado
        reg_ant_puntero = rellenar(ultimo_reg_usuario, self.longitud_puntero, tipo="izquierda")
        reg_sig_puntero = rellenar(0, self.longitud_puntero, tipo="izquierda")

        # 2. Formatear campos de datos
        num_registro_formateado = rellenar(nuevo_id_reg, self.longitud_puntero, tipo="izquierda")
        id_formateado = rellenar(id_usuario, LONGITUD_ID_USUARIO, tipo="izquierda")
        evento_formateado = rellenar(evento, self.columnas["Evento"], tipo="derecha_espacio")
        x_formateada = rellenar(x, self.columnas["X"], tipo="izquierda")
        y_formateada = rellenar(y, self.columnas["Y"], tipo="izquierda")
        
        # 3. Construir el registro completo (IDReg, IDUser, Fecha, Evento, X, Y, PtrSig, PtrAnt)
        nuevo_registro_str = (
            f"{num_registro_formateado},"
            f"{id_formateado},"
            f"{fecha},"
            f"{evento_formateado},"
            f"{x_formateada},"
            f"{y_formateada},"
            f"{reg_sig_puntero}," # Puntero siguiente
            f"{reg_ant_puntero}"  # Puntero anterior (último campo)
            f"\n"
        )
        
        nuevo_registro_bytes = nuevo_registro_str.encode('utf-8')
        if len(nuevo_registro_bytes) != self.max_fila:
             print(f"ERROR CRÍTICO DE TAMAÑO: {len(nuevo_registro_bytes)} != {self.max_fila}.")
             print(f"  Registro creado (repr): {repr(nuevo_registro_str)}")
             print(f"  Campos: ID_Reg={num_registro_formateado}, ID_User={id_formateado}, Evento={evento_formateado}, Y={y_formateada}, SIG={reg_sig_puntero}, ANT={reg_ant_puntero}")
             return None

        try:
            # Escribir el nuevo registro
            with open(self.ruta_archivo, "ab") as f:
                f.write(nuevo_registro_bytes)
                
            return nuevo_id_reg
            
        except Exception as e:
            print(f"Error al escribir el nuevo registro: {e}")
            return None
        

        try:
            # Escribir el nuevo registro
            with open(self.ruta_archivo, "ab") as f:
                f.write(nuevo_registro_bytes)
                
            return nuevo_id_reg
            
        except Exception as e:
            print(f"Error al escribir el nuevo registro: {e}")
            return None

