import pygame
pygame.init()
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, menu_opciones, fondoMenuResponsive, fuente, fuente_chica, logoMenuResponsive, link_text, link_render, link_rect

def draw_title(texto, fuente, pos, color_principal=BLANCO, color_sombra=(0,0,0)):
    sombra = fuente.render(texto, True, color_sombra)
    ventana.blit(sombra, (pos[0]+3, pos[1]+3))  
    
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        contorno = fuente.render(texto, True, (200,200,0))  
        ventana.blit(contorno, (pos[0]+dx, pos[1]+dy))

    principal = fuente.render(texto, True, color_principal)
    ventana.blit(principal, pos)



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


        logo_x = (WIDTH // 4) - (logoMenuResponsive.get_width() // 2)
        logo_y = (HEIGHT - logoMenuResponsive.get_height()) // 2
        ventana.blit(circular_surface, (logo_x, logo_y))
        

    # Column start a la derecha para el título y las opciones (aprox. 55-60% del ancho)
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







from collections import defaultdict
import datetime

def cargar_estadisticas_por_mes(path="./utils/regist/resultados.txt"):
    """
    Devuelve un diccionario: {(año, mes): [estadisticas de jugadores]}
    """
    from collections import defaultdict

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
                if len(partes) < 3:
                    continue
                uid, resultado, fecha_str = partes
                uid = int(uid)
                fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
                mes = (fecha.year, fecha.month)

                if resultado == "Ganó":
                    stats_por_mes[mes][uid]['ganados'] += 1
                elif resultado == "Perdió":
                    stats_por_mes[mes][uid]['perdidos'] += 1
                elif resultado == "Empató":
                    stats_por_mes[mes][uid]['empates'] += 1
    except FileNotFoundError:
        return {}

    # Convertir a lista de jugadores con puntos y promedio
    ranking_por_mes = {}
    usuarios_info = cargar_usuarios()  # lista de todos los usuarios

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
        jugadores.sort(key=lambda j: j["promedio"], reverse=True)
        ranking_por_mes[mes] = jugadores

    return ranking_por_mes


def cargar_usuarios(path="./utils/regist/usuarios.txt"):
    """
    Devuelve una lista de diccionarios con los datos de los usuarios:
    id, nombre
    """
    usuarios = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(",")
                if len(partes) < 2:
                    continue
                uid = int(partes[0])
                nombre = partes[1].strip()
                usuarios.append({"id": uid, "nombre": nombre})
    except FileNotFoundError:
        pass
    return usuarios

def show_ranking():
    ranking_por_mes = cargar_estadisticas_por_mes()
    if not ranking_por_mes:
        return

    meses = sorted(ranking_por_mes.keys())  # lista de (año, mes)
    indice_mes = len(meses) - 1  # empezar por el último mes

    running = True
    while running:
        ventana.blit(fondoMenuResponsive, (0,0))

        # Dibujar logo si existe
        if logoMenuResponsive:
            logo_x = (WIDTH - logoMenuResponsive.get_width()) // 2
            logo_y = 20
            ventana.blit(logoMenuResponsive, (logo_x, logo_y))

        año, mes = meses[indice_mes]
        jugadores = ranking_por_mes[(año, mes)][:10]  # top 10

        # Mostrar título con mes y año
        titulo = fuente.render(f"Ranking {mes:02d}/{año}", True, BLANCO)
        ventana.blit(titulo, ((WIDTH - titulo.get_width())//2, 30))

        # Columnas
        headers = ["#", "Jugador", "Victorias", "Derrotas", "Empates", "Puntos", "Promedio"]
        col_widths = [60, 220, 100, 100, 100, 100, 100]
        tabla_width = sum(col_widths)
        tabla_x = (WIDTH - tabla_width)//2
        col_x = [tabla_x]
        for w in col_widths[:-1]:
            col_x.append(col_x[-1]+w)

        start_y = 100
        spacing = 40

        # Dibujar encabezado
        pygame.draw.rect(ventana, (30,30,30), (tabla_x,start_y-5,tabla_width,spacing), border_radius=8)
        for j, header in enumerate(headers):
            render = fuente_chica.render(header, True, ROJO)
            ventana.blit(render, (col_x[j], start_y))

        # Dibujar filas
        for i, jugador in enumerate(jugadores, start=1):
            fila_y = start_y + i*spacing
            bg_color = (40,40,40) if i%2==0 else (25,25,25)
            pygame.draw.rect(ventana, bg_color, (tabla_x,fila_y-5,tabla_width,spacing), border_radius=6)

            color = BLANCO
            if i == 1:
                color = (255,215,0)
            elif i == 2:
                color = (192,192,192)
            elif i == 3:
                color = (205,127,50)

            datos = [
                str(i),
                jugador["nombre"],
                str(jugador["ganados"]),
                str(jugador["perdidos"]),
                str(jugador["empates"]),
                str(jugador["puntos"]),
                f"{jugador['promedio']:.2f}"
            ]
            for j, dato in enumerate(datos):
                render = fuente_chica.render(dato, True, color)
                ventana.blit(render, (col_x[j], fila_y))

        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # mes anterior
                    indice_mes = max(0, indice_mes - 1)
                elif event.key == pygame.K_RIGHT:  # mes siguiente
                    indice_mes = min(len(meses) - 1, indice_mes + 1)
                elif event.key == pygame.K_ESCAPE:  # salir
                    running = False
                elif event.key == pygame.K_SPACE:  # salir con espacio
                    return  # termina la función inmediatamente


