import pygame
import sys
pygame.init()
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, menu_opciones, fondoMenuResponsive, fuente, fuente_chica, logoMenuResponsive, link_text, link_render,menu_juego, link_rect, FPS, clock
import datetime
from collections import defaultdict
import os

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
    if logoMenuResponsive:
        radio = min(WIDTH, HEIGHT) // 5
        size = radio * 2
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        logo_x = (WIDTH // 4) - (size // 2) 
        logo_y = (HEIGHT // 2) - (size // 2) 
        
        ventana.blit(circular_surface, (logo_x, logo_y))
        
    right_start = int(WIDTH * 0.55)
    spacing = 60 
    start_y = HEIGHT // 3

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
    if logoMenuResponsive:
        radio = min(WIDTH, HEIGHT) // 5
        size = radio * 2
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        logo_x = (WIDTH // 4) - (size // 2) 
        logo_y = (HEIGHT // 2) - (size // 2) 
        
        ventana.blit(circular_surface, (logo_x, logo_y))
        
    right_start = int(WIDTH * 0.55)
    spacing = 60 
    start_y = HEIGHT // 3

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


def cargar_usuarios(path="./utils/regist/usuarios.txt"):
    usuarios = []
    
    if not os.path.exists(path):
        print(f"Advertencia: Archivo de usuarios no encontrado en {path}. Usando datos simulados.")
        return [
             {"id": 1, "nombre": "PlayerUno"},
             {"id": 2, "nombre": "Competidor2"},
             {"id": 3, "nombre": "EliasMax"}
         ]

    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                if len(partes) < 2: 
                    continue
                try:
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
    stats_por_mes = defaultdict(lambda: defaultdict(lambda: {'ganados':0,'perdidos':0,'empates':0}))

    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                
                if len(partes) < 4: 
                    continue
                
                try:
                    uid_str = partes[1].strip()
                    resultado = partes[3].strip() 
                    fecha_str = partes[2].strip()

                    uid = int(uid_str) 
                    fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
                    mes = (fecha.year, fecha.month)
                except (ValueError, IndexError):
                    print(f"Error de formato en la línea de resultado: {linea}. Ignorada.")
                    continue

                resultado_char = resultado[0].upper() if resultado else ''

                if resultado_char == "G" or resultado_char == "W" or resultado == "Ganó":
                    stats_por_mes[mes][uid]['ganados'] += 1
                elif resultado_char == "P" or resultado_char == "L" or resultado == "Perdió":
                    stats_por_mes[mes][uid]['perdidos'] += 1
                elif resultado_char == "E" or resultado_char == "D" or resultado == "Empató":
                    stats_por_mes[mes][uid]['empates'] += 1
                
    except FileNotFoundError:
        print(f"Advertencia: Archivo de resultados no encontrado en {path}. Usando datos simulados.")
        hoy = datetime.date.today()
        mes_actual = (hoy.year, hoy.month)
        
        stats_por_mes[mes_actual][1]['ganados'] = 5
        stats_por_mes[mes_actual][1]['perdidos'] = 2
        stats_por_mes[mes_actual][1]['empates'] = 1
        
        stats_por_mes[mes_actual][2]['ganados'] = 4
        stats_por_mes[mes_actual][2]['perdidos'] = 1
        stats_por_mes[mes_actual][2]['empates'] = 3
        
        stats_por_mes[mes_actual][3]['ganados'] = 6
        stats_por_mes[mes_actual][3]['perdidos'] = 4
        stats_por_mes[mes_actual][3]['empates'] = 0

    ranking_por_mes = {}
    usuarios_info = cargar_usuarios() 
    usuarios_dict = {u['id']: u['nombre'] for u in usuarios_info}

    for mes, usuarios_stats in stats_por_mes.items():
        jugadores = []
        
        for u in usuarios_info:
            uid = u['id']
            nombre = u['nombre']
            
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
            
        jugadores.sort(key=lambda j: (j["promedio"], j["puntos"]), reverse=True)
        ranking_por_mes[mes] = jugadores

    return ranking_por_mes

PANEL_COLOR = (230, 230, 230)
BAR_BASE_COLOR = (38, 43, 59)
BAR_MAX_HEIGHT = 200 
MIN_BAR_HEIGHT = 15 
COLOR_ORO = (255, 215, 0)
COLOR_PLATA = (192, 192, 192)
COLOR_BRONCE = (205, 127, 50)
BAR_COLORS = [COLOR_ORO, COLOR_PLATA, COLOR_BRONCE]
NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}
RANK_COLORS = {1: COLOR_ORO, 2: COLOR_PLATA, 3: COLOR_BRONCE}
MAX_NAME_LENGTH = 8 


def dibujar_barra_ranking(ventana, rect_panel, jugador_data, max_puntos, rank, fuente_chica):
    panel_width = rect_panel.width
    panel_height = rect_panel.height
    
    BAR_WIDTH = panel_width // 5
    BAR_SPACING = panel_width // 20
    INNER_BARS_WIDTH = 3 * BAR_WIDTH + 2 * BAR_SPACING

    START_X_BARS = rect_panel.x + (panel_width - INNER_BARS_WIDTH) // 2

    if rank == 1:
        bar_x = START_X_BARS + BAR_SPACING + BAR_WIDTH
    elif rank == 2:
        bar_x = START_X_BARS + 2 * BAR_SPACING + 2 * BAR_WIDTH
    else: 
        bar_x = START_X_BARS
        
    puntos = jugador_data.get("puntos", 0)
    
    if max_puntos > 0:
        bar_height = int((puntos / max_puntos) * BAR_MAX_HEIGHT)
    else:
        bar_height = 0
        
    bar_height = max(bar_height, MIN_BAR_HEIGHT)
        
    bar_y = rect_panel.y + panel_height - 30 - bar_height
    
    rect_barra = pygame.Rect(bar_x, bar_y, BAR_WIDTH, bar_height)
    
    color_barra = RANK_COLORS.get(rank, BAR_BASE_COLOR)
    pygame.draw.rect(ventana, color_barra, rect_barra, border_radius=5)
    
    nombre = jugador_data.get("nombre", f"User {rank}")

    if len(nombre) > MAX_NAME_LENGTH:
        nombre_visual = nombre[:MAX_NAME_LENGTH] + "..."
    else:
        nombre_visual = nombre

    render_nombre = fuente_chica.render(nombre_visual, True, BAR_BASE_COLOR) 
    
    nombre_x = bar_x + (BAR_WIDTH - render_nombre.get_width()) // 2
    nombre_y = bar_y - render_nombre.get_height() - 5
    
    ventana.blit(render_nombre, (nombre_x, nombre_y))

    puntos_val = jugador_data.get("puntos", 0)
    promedio_val = jugador_data.get("promedio", 0.0)

    render_puntos = fuente_chica.render(f"Puntos: {puntos_val}", True, BAR_BASE_COLOR)
    puntos_x = bar_x + (BAR_WIDTH - render_puntos.get_width()) // 2
    puntos_y = bar_y + bar_height + 5 
    ventana.blit(render_puntos, (puntos_x, puntos_y))

    render_promedio = fuente_chica.render(f"P: {promedio_val:.2f}", True, BAR_BASE_COLOR)
    promedio_x = bar_x + (BAR_WIDTH - render_promedio.get_width()) // 2
    promedio_y = puntos_y + render_puntos.get_height() + 2
    ventana.blit(render_promedio, (promedio_x, promedio_y))


def show_ranking(usuario_actual):
    cursor = pygame.SYSTEM_CURSOR_ARROW 
    pygame.mouse.set_cursor(cursor)
    print("ay mama no ando")
    global WIDTH, HEIGHT
    
    ranking_por_mes = cargar_estadisticas_por_mes() 
    if not ranking_por_mes:
        return

    meses = sorted(ranking_por_mes.keys())
    indice_mes = len(meses) - 1

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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size 
                
                PANEL_WIDTH = min(WIDTH * 0.7, 700)
                PANEL_HEIGHT = min(HEIGHT * 0.7, 500)
                PANEL_X = (WIDTH - PANEL_WIDTH) // 2
                PANEL_Y = (HEIGHT - PANEL_HEIGHT) // 2
                rect_panel = pygame.Rect(PANEL_X, PANEL_Y, PANEL_WIDTH, PANEL_HEIGHT)
                
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

        año, mes = meses[indice_mes]
        jugadores = ranking_por_mes[(año, mes)][:3]

        pygame.draw.rect(ventana, PANEL_COLOR, rect_panel, border_radius=15)
        
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

        max_puntos = max(j["puntos"] for j in jugadores) if jugadores else 0

        if len(jugadores) >= 3:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[2], max_puntos, 3, fuente_chica)
            
        if len(jugadores) >= 1:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[0], max_puntos, 1, fuente_chica)

        if len(jugadores) >= 2:
            dibujar_barra_ranking(ventana, rect_panel, jugadores[1], max_puntos, 2, fuente_chica)

        pygame.display.flip()
        clock.tick(FPS)