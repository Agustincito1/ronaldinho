import pygame
pygame.init()
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, menu_opciones, fondoMenuResponsive, fuente, fuente_chica

def draw_title(texto, fuente, pos, color_principal=BLANCO, color_sombra=(0,0,0)):

    sombra = fuente.render(texto, True, color_sombra)
    ventana.blit(sombra, (pos[0]+3, pos[1]+3))  
    
    for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
        contorno = fuente.render(texto, True, (200,200,0))  
        ventana.blit(contorno, (pos[0]+dx, pos[1]+dy))

    principal = fuente.render(texto, True, color_principal)
    ventana.blit(principal, pos)

def show_menu_seleccion(opcion):
    ventana.blit(fondoMenuResponsive, (0, 0))

    titulo_texto = "Ronaldinho Soccer"
    title_x = (WIDTH - fuente.size(titulo_texto)[0]) // 2
    title_y = HEIGHT // 6
    draw_title(titulo_texto, fuente, (title_x, title_y))

    spacing = 60  
    start_y = HEIGHT // 3

    for i, texto_opcion in enumerate(menu_opciones):

        color = ROJO if i == opcion else BLANCO
        opcion_render = fuente_chica.render(texto_opcion, True, color)
        opcion_x = (WIDTH - opcion_render.get_width()) // 2
        opcion_y = start_y + i * spacing

        if i == opcion:
            padding = 10
            rect = pygame.Rect(opcion_x - padding, opcion_y - padding,
                               opcion_render.get_width() + 2*padding,
                               opcion_render.get_height() + 2*padding)
            pygame.draw.rect(ventana, (50, 0, 0), rect, border_radius=8) 
        ventana.blit(opcion_render, (opcion_x, opcion_y))

    indicador = fuente_chica.render("Usa ↑ ↓ para moverte, ESPACIO para confirmar", True, BLANCO)
    ventana.blit(indicador, ((WIDTH - indicador.get_width()) // 2, start_y + len(menu_opciones)*spacing + 20))

    pygame.display.flip()
def cargar_usuarios(path="./utils/regist/usuarios.txt"):
    jugadores = []
    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            # Ejemplo: "1,Agustincito,7,4,4"
            partes = linea.split(",")
            if len(partes) < 5:
                continue  # saltar líneas mal formateadas

            uid = int(partes[0])
            nombre = partes[1].strip()
            ganados = int(partes[3])
            perdidos = int(partes[4])
            empates = int(partes[5])

            puntos = ganados * 3 + empates
            partidos = ganados + perdidos + empates
            promedio = puntos / partidos if partidos > 0 else 0

            jugadores.append({
                "id": uid,
                "nombre": nombre,
                "ganados": ganados,
                "perdidos": perdidos,
                "empates": empates,
                "puntos": puntos,
                "promedio": promedio
            })

    # Ordenar por promedio descendente
    jugadores.sort(key=lambda j: j["promedio"], reverse=True)
    return jugadores


def show_ranking():
    ventana.blit(fondoMenuResponsive, (0, 0))

    titulo = fuente.render("Ranking de Jugadores", True, BLANCO)
    title_x = (WIDTH - titulo.get_width()) // 2
    ventana.blit(titulo, (title_x, 30))
    
    jugadores = cargar_usuarios()

    headers = ["#", "Jugador", "Victorias", "Derrotas", "Empates", "Promedio"]
    col_x = [60, 140, 360, 500, 640, 820]  # posiciones X para cada columna
    start_y = 120
    spacing = 40

    pygame.draw.rect(ventana, (30, 30, 30), (50, start_y - 5, WIDTH - 100, spacing), border_radius=8)

    for j, header in enumerate(headers):
        render = fuente_chica.render(header, True, ROJO)
        ventana.blit(render, (col_x[j], start_y))

    for i, jugador in enumerate(jugadores[:10], start=1): 
        fila_y = start_y + i * spacing
        bg_color = (40, 40, 40) if i % 2 == 0 else (25, 25, 25)
        pygame.draw.rect(ventana, bg_color, (50, fila_y - 5, WIDTH - 100, spacing), border_radius=6)

        if i == 1:
            color = (255, 215, 0)  # oro
        elif i == 2:
            color = (192, 192, 192)  # plata
        elif i == 3:
            color = (205, 127, 50)  # bronce
        else:
            color = BLANCO

        datos = [
            str(i),
            jugador["nombre"],
            str(jugador["ganados"]),
            str(jugador["perdidos"]),
            str(jugador["empates"]),
            f"{jugador['promedio']:.2f}"
        ]

        for j, dato in enumerate(datos):
            render = fuente_chica.render(dato, True, color)
            ventana.blit(render, (col_x[j], fila_y))

    pygame.display.flip()
