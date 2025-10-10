import pygame
import sys
import webbrowser
from datetime import datetime
from utils.functions.gameObject import Personaje, Arco, Pelota, Contador
from utils.functions.functionMenu import show_menu_seleccion, show_ranking
from utils.functions.functionRegister import login_usuario, registro_usuario
from config import (
    BLANCO, WIDTH, HEIGHT, ventana, ROJO,
    menu_opciones, opcion, fondoResponsive,
    fuente_chica, fuente, clock, FPS,
    duracion_partido, link_rect
)
from utils.functions.othersFunction import SacarUsuario, fisicas
from gameFunctions import resetGame, gameShow, game_over_screen

# Inicializamos pygame
pygame.init()

# Crear personajes y objetos
jugador = Personaje("usuario")
bot = Personaje("bot")
arco_izquierdo = Arco("iz")
arco_derecho = Arco("dr")
pelota = Pelota()
contador = Contador(pygame.time.get_ticks(), duracion_partido, fuente_chica, BLANCO)
contador.stop(pygame.time.get_ticks())

# Variables globales
menu = True
paused = False
usuario_actual = None
goles_bot = 0
goles_jugador = 0
last_event_time = 0
fecha = datetime.now().strftime("%Y-%m-%d")
ranking = False


    
# -------------------
# LOOP PRINCIPAL
# -------------------
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor = pygame.SYSTEM_CURSOR_ARROW  # cursor por defecto
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Menú principal
        if menu:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                right_start = int(WIDTH * 0.55)
                spacing = 60
                start_y = HEIGHT // 3
                for i, texto_opcion in enumerate(menu_opciones):
                    opcion_render = fuente_chica.render(texto_opcion, True, BLANCO)
                    opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
                    opcion_y = start_y + i * spacing
                    rect = pygame.Rect(opcion_x, opcion_y, opcion_render.get_width(), opcion_render.get_height())
                    if rect.collidepoint(mouse_x, mouse_y):
                        opcion = i
                        cursor = pygame.SYSTEM_CURSOR_HAND

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # clic izquierdo
                    mouse_x, mouse_y = event.pos

                    # Clic sobre opciones del menú
                    right_start = int(WIDTH * 0.55)
                    spacing = 60
                    start_y = HEIGHT // 3
                    for i, texto_opcion in enumerate(menu_opciones):
                        opcion_render = fuente_chica.render(texto_opcion, True, BLANCO)
                        opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
                        opcion_y = start_y + i * spacing
                        rect = pygame.Rect(opcion_x, opcion_y, opcion_render.get_width(), opcion_render.get_height())

                        if rect.collidepoint(mouse_x, mouse_y):
                            opcion = i
                            # Ejecutar acción correspondiente
                            if opcion == 0:
                                usuario_actual = login_usuario()
                                if usuario_actual:
                                    pygame.mixer.music.load("./utils/music/musica.mp3")
                                    pygame.mixer.music.play(-1)
                                    menu = False
                            elif opcion == 1:
                                registro_usuario()
                            elif opcion == 2:
                                show_ranking()
                                ranking = True
                                menu = False
                                if show_ranking() != True:
                                    ranking = False
                                    menu = True
                            elif opcion == 3:
                                pygame.quit()
                                sys.exit()

                    # Clic sobre el link de GitHub
                    if link_rect.collidepoint(mouse_x, mouse_y):
                        webbrowser.open("https://github.com/Agustincito1")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                opcion = (opcion - 1) % len(menu_opciones)
            if event.key == pygame.K_DOWN:
                opcion = (opcion + 1) % len(menu_opciones)
            if event.key == pygame.K_RETURN:

                if opcion == 0:
                    usuario_actual = login_usuario()
                    if usuario_actual:
                        pygame.mixer.music.load("./utils/music/musica.mp3")
                        pygame.mixer.music.play(-1)
                        menu = False
                elif opcion == 1:
                    registro_usuario()
                elif opcion == 2:
                    show_ranking()
                    ranking = True
                    menu = False
                    if show_ranking() != True:
                        ranking = False
                        menu = True
                elif opcion == 3:
                    pygame.quit()
                    sys.exit()
        else:  # juego en curso
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota)
                    menu = True
                    paused = False
                    ranking = False
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        contador.stop(pygame.time.get_ticks())
                    else:
                        contador.resume(pygame.time.get_ticks())

    # =======================
    # CONTROL DE CURSOR GLOBAL
    # =======================
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if menu:
        
        # Hover sobre opciones del menú
        right_start = int(WIDTH * 0.55)
        spacing = 60
        start_y = HEIGHT // 3
        for i, texto_opcion in enumerate(menu_opciones):
            opcion_render = fuente_chica.render(texto_opcion, True, BLANCO)
            opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
            opcion_y = start_y + i * spacing
            rect = pygame.Rect(opcion_x, opcion_y, opcion_render.get_width(), opcion_render.get_height())
            if rect.collidepoint(mouse_x, mouse_y):
                cursor = pygame.SYSTEM_CURSOR_HAND

        # Hover sobre el link de GitHub
        if link_rect.collidepoint(mouse_x, mouse_y):
            cursor = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor)

        
        pygame.mouse.set_cursor(cursor)
        show_menu_seleccion(opcion, mouse_x, mouse_y)


        pygame.display.flip()
        continue

    # =======================
    # RANKING
    # =======================
    if ranking:
        show_ranking()
        continue

    # =======================
    # PAUSA
    # =======================
    if paused:
        ventana.blit(fondoResponsive, (0, 0))
        texto = fuente.render("|| Juego en Pausa", True, ROJO)
        ventana.blit(texto, ((WIDTH - texto.get_width()) // 2, HEIGHT // 2))
        marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, ROJO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, 30))
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # =======================
    # JUEGO EN CURSO
    # =======================
    keys = pygame.key.get_pressed()
    jugador.mover(keys)
    bot.mover_bot(pelota)
    fisicas(jugador, bot, pelota)
    menu = gameShow(usuario_actual, goles_bot, goles_jugador, last_event_time,
                    jugador, bot, pelota, contador, arco_izquierdo, arco_derecho)

    clock.tick(FPS)
