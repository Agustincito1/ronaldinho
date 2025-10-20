import pygame
pygame.init()
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, menu_opciones, fondoMenuResponsive, fuente, fuente_chica, logoMenuResponsive, link_text, link_render,menu_juego, link_rect, FPS, clock

def draw_title(texto, fuente, pos, color_principal=BLANCO, color_sombra=(0,0,0)):
    sombra = fuente.render(texto, True, color_sombra)
    ventana.blit(sombra, (pos[0]+3, pos[1]+3))  
    
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        contorno = fuente.render(texto, True, (200,200,0))  
        ventana.blit(contorno, (pos[0]+dx, pos[1]+dy))

    principal = fuente.render(texto, True, color_principal)
    ventana.blit(principal, pos)


def show_menu_juego(opcion, mouse_x, mouse_y, usuario):


    ventana.blit(fondoMenuResponsive, (0, 0))
    # Dibujar logo si existe: centrar verticalmente y colocarlo hacia la izquierda (1/4 del ancho)
    if logoMenuResponsive:
        radio = min(WIDTH, HEIGHT) // 5
        size = radio * 2
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # --- CORRECCIÓN AQUÍ ---
        # Usamos 'size' (el ancho/alto del logo escalado) para centrar.
        logo_x = (WIDTH // 4) - (size // 2) 
        logo_y = (HEIGHT // 2) - (size // 2) # Centrar verticalmente usando 'size'
        
        ventana.blit(circular_surface, (logo_x, logo_y))
        
    # Column start a la derecha para el título y las opciones (aprox. 55-60% del ancho)
    right_start = int(WIDTH * 0.55)
    spacing = 60  
    start_y = HEIGHT // 3

    # ... (El resto de la función sigue igual)
    for i, texto_opcion in enumerate(menu_juego):

        color = BLANCO
        opcion_render = fuente_chica.render(texto_opcion, True, color)
        opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
        opcion_y = start_y + i * spacing
        if i == opcion:
            padding = 10
            rect = pygame.Rect(opcion_x - padding, opcion_y - padding,
                                opcion_render.get_width() + 2*padding,
                                opcion_render.get_height() + 2*padding)
            pygame.draw.rect(ventana, (50, 0, 0), rect, border_radius=8) 
        ventana.blit(opcion_render, (opcion_x, opcion_y));

    if link_rect.collidepoint(mouse_x, mouse_y):
        link_color = (180, 220, 255)
        link_render = fuente_chica.render(link_text, True, (180, 220, 255))
    else:
        link_color = (100, 150, 255)
        link_render = fuente_chica.render(link_text, True, (100, 150, 255))

    ventana.blit(link_render, link_rect)

    pygame.display.flip()








def show_menu_seleccion(opcion, mouse_x, mouse_y):


    ventana.blit(fondoMenuResponsive, (0, 0))
    # Dibujar logo si existe: centrar verticalmente y colocarlo hacia la izquierda (1/4 del ancho)
    if logoMenuResponsive:
        radio = min(WIDTH, HEIGHT) // 5
        size = radio * 2
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # --- CORRECCIÓN AQUÍ ---
        # Usamos 'size' (el ancho/alto del logo escalado) para centrar.
        logo_x = (WIDTH // 4) - (size // 2) 
        logo_y = (HEIGHT // 2) - (size // 2) # Centrar verticalmente usando 'size'
        
        ventana.blit(circular_surface, (logo_x, logo_y))
        
    # Column start a la derecha para el título y las opciones (aprox. 55-60% del ancho)
    right_start = int(WIDTH * 0.55)
    spacing = 60  
    start_y = HEIGHT // 3

    # ... (El resto de la función sigue igual)
    for i, texto_opcion in enumerate(menu_opciones):

        color = BLANCO
        opcion_render = fuente_chica.render(texto_opcion, True, color)
        opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
        opcion_y = start_y + i * spacing
        if i == opcion:
            padding = 10
            rect = pygame.Rect(opcion_x - padding, opcion_y - padding,
                                opcion_render.get_width() + 2*padding,
                                opcion_render.get_height() + 2*padding)
            pygame.draw.rect(ventana, (50, 0, 0), rect, border_radius=8) 
        ventana.blit(opcion_render, (opcion_x, opcion_y));

    if link_rect.collidepoint(mouse_x, mouse_y):
        link_color = (180, 220, 255)
        link_render = fuente_chica.render(link_text, True, (180, 220, 255))
    else:
        link_color = (100, 150, 255)
        link_render = fuente_chica.render(link_text, True, (100, 150, 255))

    ventana.blit(link_render, link_rect)

    pygame.display.flip()


import datetime
from collections import defaultdict
import os # Necesario para verificar si el archivo existe

def cargar_usuarios(path="./utils/regist/usuarios.txt"):
    """
    Devuelve una lista de diccionarios con los datos de los usuarios:
    id, nombre
    Añade datos simulados si el archivo no existe para evitar fallos.
    """
    usuarios = []
    
    # --- MODIFICACIÓN: Si el archivo no existe, usamos datos simulados ---
    if not os.path.exists(path):
         print(f"Advertencia: Archivo de usuarios no encontrado en {path}. Usando datos simulados.")
         return [
            {"id": 1, "nombre": "PlayerUno"},
            {"id": 2, "nombre": "Competidor2"},
            {"id": 3, "nombre": "EliasMax"}
        ]
    # ---------------------------------------------------------------------

    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                # El archivo de usuario puede tener más de 2 partes (ej: ID, Nombre, Contraseña)
                if len(partes) < 2: 
                    continue
                try:
                    # Se incluye try/except aquí para manejar líneas mal formadas
                    # Se usa strip() en partes[0] para manejar UIDs con posible padding
                    uid = int(partes[0].strip()) 
                    nombre = partes[1].strip()
                    usuarios.append({"id": uid, "nombre": nombre})
                except ValueError:
                    print(f"Error al parsear línea de usuario: {linea}. Ignorada.")
                    continue
    except Exception as e:
        print(f"Error general al cargar usuarios: {e}. Devolviendo lista vacía.")
        pass 
    return usuarios


def cargar_estadisticas_por_mes(path="./utils/regist/resultados.txt"):
    """
    Devuelve un diccionario: {(año, mes): [estadisticas de jugadores]}
    Acepta resultados como "Ganó", "Perdió", "Empató" o sus abreviaturas de una letra
    (G/W, P/L, E/D).
    """
    
    # Diccionario: (año, mes) -> id_usuario -> {'ganados':..., 'perdidos':..., 'empates':...}
    stats_por_mes = defaultdict(lambda: defaultdict(lambda: {'ganados':0,'perdidos':0,'empates':0}))

    # Leer resultados
    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                # El archivo de resultados del usuario tiene 5 partes. Solo necesitamos las primeras 3.
                if len(partes) < 3: 
                    continue
                
                # Desempaquetado seguro y conversión de tipos
                try:
                    # Tomamos las primeras tres partes, ignorando las demás (00000, 00000)
                    uid_str, resultado, fecha_str = partes[0].strip(), partes[1].strip(), partes[2].strip()
                    
                    # El UID puede venir con padding ('02')
                    uid = int(uid_str) 
                    fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
                    mes = (fecha.year, fecha.month)
                except (ValueError, IndexError):
                    print(f"Error de formato en la línea de resultado: {linea}. Ignorada.")
                    continue

                # --- LÓGICA MODIFICADA PARA ACEPTAR LETRAS (E) O PALABRAS COMPLETAS ---
                resultado_char = resultado[0].upper() if resultado else ''

                if resultado == "Ganó" or resultado_char == "G" or resultado_char == "W":
                    stats_por_mes[mes][uid]['ganados'] += 1
                elif resultado == "Perdió" or resultado_char == "P" or resultado_char == "L":
                    stats_por_mes[mes][uid]['perdidos'] += 1
                elif resultado == "Empató" or resultado_char == "E" or resultado_char == "D":
                    stats_por_mes[mes][uid]['empates'] += 1
                # ----------------------------------------------------------------------
                
    except FileNotFoundError:
        # --- MODIFICACIÓN: Si el archivo no existe, usamos datos simulados ---
        print(f"Advertencia: Archivo de resultados no encontrado en {path}. Usando datos simulados.")
        hoy = datetime.date.today()
        mes_actual = (hoy.year, hoy.month)
        
        # Datos simulados (utilizando IDs 1, 2, 3 de cargar_usuarios)
        stats_por_mes[mes_actual][1]['ganados'] = 5
        stats_por_mes[mes_actual][1]['perdidos'] = 2
        stats_por_mes[mes_actual][1]['empates'] = 1
        
        stats_por_mes[mes_actual][2]['ganados'] = 4
        stats_por_mes[mes_actual][2]['perdidos'] = 1
        stats_por_mes[mes_actual][2]['empates'] = 3
        
        stats_por_mes[mes_actual][3]['ganados'] = 6
        stats_por_mes[mes_actual][3]['perdidos'] = 4
        stats_por_mes[mes_actual][3]['empates'] = 0
        # ---------------------------------------------------------------------

    # Convertir a lista de jugadores con puntos y promedio
    ranking_por_mes = {}
    usuarios_info = cargar_usuarios() 
    usuarios_dict = {u['id']: u['nombre'] for u in usuarios_info}

    for mes, usuarios_stats in stats_por_mes.items():
        jugadores = []
        
        # Iteramos sobre TODOS los usuarios, no solo los que tienen resultados este mes
        # Esto asegura que si un usuario tiene 0 partidas, aún aparece en el ranking.
        for u in usuarios_info:
            uid = u['id']
            nombre = u['nombre']
            
            # Usar .get() para obtener 0s si el usuario no tiene estadísticas este mes
            stats = usuarios_stats.get(uid, {'ganados':0,'perdidos':0,'empates':0})
            
            puntos = stats['ganados']*3 + stats['empates']
            partidos = stats['ganados'] + stats['perdidos'] + stats['empates']
            promedio = puntos / partidos if partidos > 0 else 0
            
            jugadores.append({
                "id": uid,
                "nombre": nombre,
                "ganados": stats['ganados'],
                "perdidos": stats['perdidos'],
                "empates": stats['empates'],
                "puntos": puntos,
                "promedio": promedio
            })
            
        # Ordenar por promedio (descendente)
        jugadores.sort(key=lambda j: (j["promedio"], j["puntos"]), reverse=True)
        ranking_por_mes[mes] = jugadores

    return ranking_por_mes

# --- Nuevas Constantes de Estilo para el Ranking ---
PANEL_COLOR = (230, 230, 230)
BAR_BASE_COLOR = (38, 43, 59)
BAR_MAX_HEIGHT = 200 # Altura máxima de la barra en píxeles

# Colores para el Top 3 (similares a la imagen/metales)
PANEL_COLOR = (230, 230, 230)
BAR_BASE_COLOR = (38, 43, 59)
BAR_MAX_HEIGHT = 200 
MIN_BAR_HEIGHT = 15 # <--- ¡ESTA ES LA CONSTANTE QUE FALTABA!
COLOR_ORO = (255, 215, 0)
COLOR_PLATA = (192, 192, 192)
COLOR_BRONCE = (205, 127, 50)
BAR_COLORS = [COLOR_ORO, COLOR_PLATA, COLOR_BRONCE]


NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
# Colores de Podio
COLOR_ORO = (255, 215, 0)
COLOR_PLATA = (192, 192, 192)
COLOR_BRONCE = (205, 127, 50)
BAR_BASE_COLOR = (38, 43, 59)
MIN_BAR_HEIGHT = 15
BAR_MAX_HEIGHT = 200 

# Nuevo mapeo para la asignación de color por puesto
RANK_COLORS = {1: COLOR_ORO, 2: COLOR_PLATA, 3: COLOR_BRONCE}

# Máxima longitud del nombre antes de truncar
MAX_NAME_LENGTH = 8 


def dibujar_barra_ranking(ventana, rect_panel, jugador_data, max_puntos, rank, fuente_chica):
    """
    Dibuja una barra individual con su etiqueta, nombre y estadísticas dentro del panel.
    """
    panel_width = rect_panel.width
    panel_height = rect_panel.height
    
    # --- 1. Cálculo de Posición (CENTRADOS) ---
    BAR_WIDTH = panel_width // 5
    BAR_SPACING = panel_width // 20
    INNER_BARS_WIDTH = 3 * BAR_WIDTH + 2 * BAR_SPACING

    START_X_BARS = rect_panel.x + (panel_width - INNER_BARS_WIDTH) // 2

    # El orden visual es: 3º (Izquierda), 1º (Centro), 2º (Derecha)
    if rank == 1:
        bar_x = START_X_BARS + BAR_SPACING + BAR_WIDTH
    elif rank == 2:
        bar_x = START_X_BARS + 2 * BAR_SPACING + 2 * BAR_WIDTH
    else: # rank == 3
        bar_x = START_X_BARS
        
    # --- 2. Cálculo de Altura y Mínimo de 15px ---
    puntos = jugador_data.get("puntos", 0)
    
    if max_puntos > 0:
        bar_height = int((puntos / max_puntos) * BAR_MAX_HEIGHT)
    else:
        bar_height = 0
        
    bar_height = max(bar_height, MIN_BAR_HEIGHT)
        
    bar_y = rect_panel.y + panel_height - 30 - bar_height
    
    rect_barra = pygame.Rect(bar_x, bar_y, BAR_WIDTH, bar_height)
    
    # 3. Dibujar la barra - ASIGNACIÓN DE COLOR CORREGIDA
    color_barra = RANK_COLORS.get(rank, BAR_BASE_COLOR)
    pygame.draw.rect(ventana, color_barra, rect_barra, border_radius=5)
    
    # 4. Dibujar la etiqueta (Nombre) - CORRECCIÓN DE NOMBRES LARGOS
    nombre = jugador_data.get("nombre", f"User {rank}")

    if len(nombre) > MAX_NAME_LENGTH:
        nombre_visual = nombre[:MAX_NAME_LENGTH] + "..."
    else:
        nombre_visual = nombre

    render_nombre = fuente_chica.render(nombre_visual, True, BAR_BASE_COLOR) 
    
    nombre_x = bar_x + (BAR_WIDTH - render_nombre.get_width()) // 2
    nombre_y = bar_y - render_nombre.get_height() - 5
    
    ventana.blit(render_nombre, (nombre_x, nombre_y))

    # 5. Dibujar ESTADÍSTICAS ADICIONALES
    puntos_val = jugador_data.get("puntos", 0)
    promedio_val = jugador_data.get("promedio", 0.0)

    # Display Puntos
    render_puntos = fuente_chica.render(f"Puntos: {puntos_val}", True, BAR_BASE_COLOR)
    puntos_x = bar_x + (BAR_WIDTH - render_puntos.get_width()) // 2
    puntos_y = bar_y + bar_height + 5 
    ventana.blit(render_puntos, (puntos_x, puntos_y))

    # Display Promedio
    render_promedio = fuente_chica.render(f"P: {promedio_val:.2f}", True, BAR_BASE_COLOR)
    promedio_x = bar_x + (BAR_WIDTH - render_promedio.get_width()) // 2
    promedio_y = puntos_y + render_puntos.get_height() + 2
    ventana.blit(render_promedio, (promedio_x, promedio_y))



def show_ranking(usuario_actual):
    cursor = pygame.SYSTEM_CURSOR_ARROW  
    pygame.mouse.set_cursor(cursor)
    # Declaraciones globales (si se van a modificar en la función)
    global WIDTH, HEIGHT
    
    # Asumiendo que 'cargar_estadisticas_por_mes' existe
    ranking_por_mes = cargar_estadisticas_por_mes() 
    if not ranking_por_mes:
        return

    meses = sorted(ranking_por_mes.keys())
    indice_mes = len(meses) - 1

    # --- Geometría (Inicial) ---
    PANEL_WIDTH = min(WIDTH * 0.7, 700)
    PANEL_HEIGHT = min(HEIGHT * 0.7, 500)
    PANEL_X = (WIDTH - PANEL_WIDTH) // 2
    PANEL_Y = (HEIGHT - PANEL_HEIGHT) // 2
    rect_panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
    
    LOGO_MARGIN = 20
    LOGO_SIZE = min(WIDTH, HEIGHT) // 5 
    LOGO_X = LOGO_MARGIN
    LOGO_Y = LOGO_MARGIN

    running = True
    while running:
        # 1. Manejo de Eventos (Incluye Redimensionamiento)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size 
                
                # Recalcular geometría de ranking
                PANEL_WIDTH = min(WIDTH * 0.7, 700)
                PANEL_HEIGHT = min(HEIGHT * 0.7, 500)
                PANEL_X = (WIDTH - PANEL_WIDTH) // 2
                PANEL_Y = (HEIGHT - PANEL_HEIGHT) // 2
                rect_panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
                
                # Recalcular geometría del logo
                LOGO_SIZE = min(WIDTH, HEIGHT) // 5
                LOGO_X = LOGO_MARGIN
                LOGO_Y = LOGO_MARGIN


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    indice_mes = max(0, indice_mes - 1)
                elif event.key == pygame.K_RIGHT:
                    indice_mes = min(len(meses) - 1, indice_mes + 1)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    return
        
        # 2. Dibujado de Fondo y Logo
        ventana.blit(fondoMenuResponsive, (0,0))
        
        if logoMenuResponsive:
            size = LOGO_SIZE
            radio = size // 2
            
            Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
            circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            mask = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
            circular_surface.blit(Imagen, (0, 0))
            circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            ventana.blit(circular_surface, (LOGO_X, LOGO_Y))

        # 3. Obtener datos, mes y dibujar el panel
        año, mes = meses[indice_mes]
        jugadores = ranking_por_mes[(año, mes)][:3] # Top 3

        pygame.draw.rect(ventana, PANEL_COLOR, rect_panel, border_radius=15)
        
        # 4. Título con el Mes/Año Correcto
        mes_str = NOMBRES_MESES.get(mes, f"Mes {mes}")
        mes_nombre_completo = f"{mes_str} {año}"
        
        titulo = fuente.render(mes_nombre_completo, True, BLANCO)
        
        titulo_padding = 15
        titulo_rect = pygame.Rect(PANEL_X + (PANEL_WIDTH - titulo.get_width() - titulo_padding*2)//2, 
                                  PANEL_Y - titulo.get_height(), 
                                  titulo.get_width() + titulo_padding*2, 
                                  titulo.get_height() + titulo_padding)
        pygame.draw.rect(ventana, BAR_BASE_COLOR, titulo_rect, border_radius=10)
        
        ventana.blit(titulo, (titulo_rect.x + titulo_padding, titulo_rect.y + titulo_padding//2))

        # 5. Dibujar barras
        max_puntos = max(j["puntos"] for j in jugadores) if jugadores else 0

        # Orden de dibujo: 3º, 1º, 2º
        if len(jugadores) >= 3:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[2], max_puntos, 3, fuente_chica)
            
        if len(jugadores) >= 1:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[0], max_puntos, 1, fuente_chica)

        if len(jugadores) >= 2:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[1], max_puntos, 2, fuente_chica)

        pygame.display.flip()
        clock.tick(FPS)