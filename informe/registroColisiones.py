from collections import defaultdict
import os
import pygame
import sys

# --- CONFIGURACIÓN DE RUTAS Y LONGITUD FIJA (Copiado del archivo de registro) ---
# Usamos las mismas constantes que el módulo de funciones para asegurar la consistencia.
LONGITUD_ID_RESUMEN = 2      
LONGITUD_CONTADOR = 5        
RUTA_USUARIOS = "./utils/regist/usuarios.txt"
RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"
RUTA_RESUMEN = "./utils/regist/resumen.txt"

# ------------------- FUNCIONES DE LÓGICA DE DATOS INTEGRADA -------------------
# Se integran aquí para hacer el archivo Pygame autocontenido y eliminar la necesidad
# de importar de 'funciones.py' o 'resumen_colisiones.py'.

def sacar_usuario(user_id):
    """
    Función para extraer el nombre del usuario dado su ID.
    Utiliza RUTA_USUARIOS.
    """
    usuario = "ID Desconocido"
    try:
        # Usamos la constante RUTA_USUARIOS
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                # El ID debe coincidir
                if len(partes) >= 1 and int(partes[0]) == int(user_id):
                    if len(partes) >= 2:
                        # Strip para limpiar los posibles espacios de relleno del nombre
                        usuario = partes[1].strip() 
                        return usuario
    except FileNotFoundError:
        # En una aplicación Pygame real, esto debería manejar el error de forma visual
        return usuario
    except ValueError:
        # Manejo de IDs no válidos
        return usuario
    return usuario


def resumenCol():
    """
    Lee todos los registros de eventos, cuenta las colisiones por tipo 
    para cada ID de usuario y escribe el resumen en RUTA_RESUMEN.
    """
    
    # 1. Leer usuarios para obtener solo los IDs válidos
    usuarios_ids = set()
    try:
        if not os.path.exists(RUTA_USUARIOS):
            print(f"⚠️ Archivo de usuarios no encontrado en {RUTA_USUARIOS}.")
            return
            
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) >= 1 and partes[0]:
                    usuarios_ids.add(partes[0].zfill(LONGITUD_ID_RESUMEN)) 
    except Exception:
        return

    # 2. Diccionario con la estructura de conteo
    resumen = defaultdict(lambda: {
        "Pelota": 0, "ArcoDerecho": 0, "ArcoIzquierdo": 0, "Bot": 0
    })

    # 3. Leer registros de eventos y acumular
    try:
        if not os.path.exists(RUTA_REGISTRO_EVENTOS):
             print(f"⚠️ Archivo de registro de eventos no encontrado en {RUTA_REGISTRO_EVENTOS}.")
             # Si el archivo no existe, el resumen queda vacío, lo cual es correcto.
        else:
            with open(RUTA_REGISTRO_EVENTOS, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(",") 
                    if len(partes) < 3:
                        continue
                        
                    id_usuario = partes[0].zfill(LONGITUD_ID_RESUMEN)
                    tipo_evento = partes[2].strip() 
                    
                    if id_usuario in usuarios_ids and tipo_evento in resumen[id_usuario]:
                        resumen[id_usuario][tipo_evento] += 1
    
    except Exception:
        pass


    # 4. Guardar resumen en formato de LONGITUD FIJA
    try:
        # Aseguramos que la carpeta exista antes de escribir
        os.makedirs(os.path.dirname(RUTA_RESUMEN), exist_ok=True)
        with open(RUTA_RESUMEN, "w", encoding="utf-8") as f:
            for id_usuario in sorted(list(usuarios_ids)):
                datos = resumen[id_usuario]
                
                pelota = str(datos['Pelota']).zfill(LONGITUD_CONTADOR)
                arco_derecho = str(datos['ArcoDerecho']).zfill(LONGITUD_CONTADOR)
                arco_izquierdo = str(datos['ArcoIzquierdo']).zfill(LONGITUD_CONTADOR)
                bot = str(datos['Bot']).zfill(LONGITUD_CONTADOR)
                
                f.write(
                    f"{id_usuario},"
                    f"{pelota},"
                    f"{arco_derecho},"
                    f"{arco_izquierdo},"
                    f"{bot}\n"
                )
    except Exception as e:
        print(f"❌ Error al escribir el archivo resumen: {e}")

# ------------------- INICIALIZACIÓN PYGAME -------------------

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("📊 Registro de Colisiones")

# Fuentes y colores
font = pygame.font.SysFont("consolas", 28, bold=True)
big_font = pygame.font.SysFont("consolas", 40, bold=True)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
YELLOW = (255, 215, 0)
GREEN_LIME = (50, 205, 50) # Usamos un nombre más descriptivo para el verde
BG_COLOR = (25, 25, 25)
BOX_COLOR = (45, 45, 45)
HIGHLIGHT_COLOR = (70, 70, 70)

# Opciones del menú
options = ["📂 Ver registro de los usuarios",
           "🔎 Año y mes usuario específico"]
selected = 0


# ------------------- DIBUJAR MENÚ -------------------
def draw_menu():
    screen.fill(BG_COLOR)
    title = big_font.render("MENÚ PRINCIPAL", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    for i, option in enumerate(options):
        color = YELLOW if i == selected else GRAY
        bg_rect = pygame.Rect(100, 150 + i * 80, WIDTH - 200, 60)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR if i == selected else BOX_COLOR, bg_rect, border_radius=10)
        text = font.render(option, True, color)
        screen.blit(text, (bg_rect.x + 20, bg_rect.y + 15))

    pygame.display.flip()


# ------------------- MOSTRAR RESUMEN (OPCIÓN 1) -------------------
def mostrar_resumen():
    # 1. Genera el archivo resumen.txt usando la lógica de longitud fija
    resumenCol() 
    
    lineas_datos = []
    try:
        # 2. Lee el archivo generado
        with open(RUTA_RESUMEN, "r", encoding="utf-8") as f:
            raw_lineas = f.readlines()
            
        # 3. Formatear datos, incluyendo el nombre de usuario
        for linea in raw_lineas:
            # Formato: ID(2),Pelota(5),ArcoDerecho(5),ArcoIzquierdo(5),Bot(5)
            partes_raw = linea.strip().split(",")
            if len(partes_raw) == 5:
                user_id = partes_raw[0]
                nombre = sacar_usuario(user_id) # Uso de la función integrada
                
                # Crear la lista de 6 elementos: [ID, Nombre, Pelota, ArcoD, ArcoI, Bot]
                # Los valores numéricos vienen con ZFILL, se deben mostrar sin ceros a la izquierda
                lineas_datos.append([
                    user_id, 
                    nombre, 
                    str(int(partes_raw[1])), # Pelota
                    str(int(partes_raw[2])), # ArcoDerecho
                    str(int(partes_raw[3])), # ArcoIzquierdo
                    str(int(partes_raw[4]))  # Bot
                ])
                
    except FileNotFoundError:
        lineas_datos = [] 

    running = True
    # Ajustar col_widths para la columna de Nombre
    col_widths = [80, 250, 100, 100, 100, 100]  # ID, Nombre, Pelota, ArcoD, ArcoI, Bot
    x_start = 50
    row_height = 38
    header_bg = (35, 35, 60)
    even_row_bg = (40, 40, 40)
    odd_row_bg = (55, 55, 55)
    border_color = (90, 90, 90)

    while running:
        screen.fill(BG_COLOR)
        header = big_font.render("📊 Resumen de Todos los Usuarios", True, GREEN_LIME)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        y = 100
        # Dibujar fondo del encabezado
        pygame.draw.rect(screen, header_bg, (x_start, y, sum(col_widths), row_height), border_radius=8)
        # Dibujar encabezados de columna
        encabezados = ["ID", "Nombre", "Pelota", "ArcoD", "ArcoI", "Bot"]
        x = x_start
        for i, enc in enumerate(encabezados):
            text = font.render(enc, True, YELLOW)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[i]
        y += row_height

        # Dibujar filas de datos
        for idx, partes in enumerate(lineas_datos):
            if len(partes) == 6: 
                row_bg = even_row_bg if idx % 2 == 0 else odd_row_bg
                pygame.draw.rect(screen, row_bg, (x_start, y, sum(col_widths), row_height))
                # Dibujar borde inferior
                pygame.draw.line(screen, border_color, (x_start, y + row_height), (x_start + sum(col_widths), y + row_height), 2)
                
                x = x_start
                for i, valor in enumerate(partes):
                    color = WHITE
                    if i == 1: # Nombre
                        color = YELLOW
                    elif i > 1 and int(valor) > 0: # Contadores > 0
                        color = GREEN_LIME
                        
                    text_surface = font.render(valor, True, color)
                    if i >= 2:
                        # Centrar texto en la columna para los contadores
                        text_x = x + col_widths[i] // 2 - text_surface.get_width() // 2
                    else:
                        # Alinear a la izquierda
                        text_x = x + 10
                        
                    screen.blit(text_surface, (text_x, y + 5))
                    x += col_widths[i]
                y += row_height

        # Dibujar borde exterior de la tabla
        pygame.draw.rect(screen, border_color, (x_start, 100, sum(col_widths), y - 100), 3, border_radius=10)
        
        # Botón de escape/volver
        back_text = font.render("Presione ESC para volver al menú", True, GRAY)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 40))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# ------------------- INPUT DE TEXTO -------------------
def pedir_texto_pygame(mensaje):
    texto = ""
    activo = True
    
    # Bucle para asegurar que el cuadro de texto se muestra correctamente
    while activo:
        screen.fill(BG_COLOR)
        
        # Título del prompt
        title = big_font.render("Entrada de Datos", True, YELLOW)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        prompt = font.render(mensaje, True, WHITE)
        screen.blit(prompt, (50, 150))

        caja = pygame.Rect(50, 200, 300, 50) # Hacemos la caja más pequeña
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, caja, border_radius=8)
        
        input_text = font.render(texto, True, YELLOW)
        screen.blit(input_text, (caja.x + 10, caja.y + 10))
        
        # Indicación de tecla
        enter_text = font.render("Presione ENTER para continuar", True, GRAY)
        screen.blit(enter_text, (50, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif event.unicode.isprintable():
                    texto += event.unicode
    return texto.strip()


# ------------------- REGISTRO POR AÑO Y MES (OPCIÓN 2) -------------------
def mostrar_registro_por_anio_mes():
    
    # 1. Pedir ID y Año
    usuario_id = pedir_texto_pygame("Ingrese el ID del usuario: ")
    anio = pedir_texto_pygame("Ingrese el año (ej: 2025): ")
    
    # 2. Validar y obtener nombre
    try:
        if not usuario_id or not anio: return
        int(usuario_id)
        int(anio)
    except ValueError:
        # Aquí se mostraría un error visual en una versión completa.
        return

    usuario_nombre = sacar_usuario(usuario_id) # Uso de la función integrada
    
    # Estructura de conteo mensual por tipo de evento
    meses_conteo = defaultdict(lambda: {"Pelota": 0, "ArcoDerecho": 0, "ArcoIzquierdo": 0, "Bot": 0})
    
    nombres_meses = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio",
        "07": "Julio", "08": "Agosto", "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }

    # 3. Leer y procesar registros
    try:
        if not os.path.exists(RUTA_REGISTRO_EVENTOS):
            return
            
        with open(RUTA_REGISTRO_EVENTOS, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",")
                if len(partes) < 3:
                    continue
                    
                id_usuario, fecha, tipo_raw = partes[:3]
                tipo = tipo_raw.strip() # El tipo debe estar limpio
                
                # Comparamos IDs asegurando que ambos estén normalizados (con zfill)
                if id_usuario.zfill(LONGITUD_ID_RESUMEN) == usuario_id.zfill(LONGITUD_ID_RESUMEN) and fecha.startswith(anio):
                    try:
                        mes = fecha.split("-")[1]
                        if mes in nombres_meses and tipo in meses_conteo[mes]:
                            meses_conteo[mes][tipo] += 1
                    except IndexError:
                        pass
    except Exception:
        pass # Manejo de errores de archivo

    # 4. Dibujar la tabla
    running = True
    col_widths = [200, 120, 120, 120, 120]  # Mes, Pelota, ArcoD, ArcoI, Bot
    x_start = 50
    row_height = 38
    header_bg = (35, 35, 60)
    even_row_bg = (40, 40, 40)
    odd_row_bg = (55, 55, 55)
    border_color = (90, 90, 90)

    while running:
        screen.fill(BG_COLOR)
        header = big_font.render(f"📅 Colisiones de {usuario_nombre} en {anio}", True, GREEN_LIME)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        y = 100
        # Dibujar encabezados
        pygame.draw.rect(screen, header_bg, (x_start, y, sum(col_widths), row_height), border_radius=8)
        encabezados = ["Mes", "Pelota", "ArcoD", "ArcoI", "Bot"]
        x = x_start
        for i, enc in enumerate(encabezados):
            text_surface = font.render(enc, True, YELLOW)
            screen.blit(text_surface, (x + 10, y + 5))
            x += col_widths[i]
        y += row_height

        # Dibujar filas de datos
        # Iteramos sobre los meses en orden
        for idx, mes_num in enumerate(nombres_meses.keys()):
            datos = meses_conteo[mes_num]
            
            row_bg = even_row_bg if idx % 2 == 0 else odd_row_bg
            pygame.draw.rect(screen, row_bg, (x_start, y, sum(col_widths), row_height))
            pygame.draw.line(screen, border_color, (x_start, y + row_height), (x_start + sum(col_widths), y + row_height), 2)
            
            x = x_start
            
            # Mes (columna 0)
            nombre_mes = nombres_meses.get(mes_num, mes_num)
            text_surface = font.render(nombre_mes, True, WHITE)
            screen.blit(text_surface, (x + 10, y + 5))
            x += col_widths[0]
            
            # Contadores (columnas 1 a 4)
            contadores = [datos['Pelota'], datos['ArcoDerecho'], datos['ArcoIzquierdo'], datos['Bot']]
            for i in range(4):
                valor = contadores[i]
                color = GREEN_LIME if valor > 0 else GRAY
                
                text_surface = font.render(str(valor), True, color)
                # Centrar texto en la columna
                text_x = x + col_widths[i+1] // 2 - text_surface.get_width() // 2
                screen.blit(text_surface, (text_x, y + 5))
                x += col_widths[i+1]
                
            y += row_height

        # Dibujar borde exterior de la tabla
        pygame.draw.rect(screen, border_color, (x_start, 100, sum(col_widths), y - 100), 3, border_radius=10)
        
        # Botón de escape/volver
        back_text = font.render("Presione ESC para volver al menú", True, GRAY)
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# ------------------- LOOP PRINCIPAL -------------------
if __name__ == '__main__':
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        mostrar_resumen()
                    elif selected == 1:
                        mostrar_registro_por_anio_mes()
