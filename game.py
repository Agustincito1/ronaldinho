import pygame
import sys
import webbrowser
from iaMens import show_preguntas
from datetime import datetime
from shop import mostrar_mercado_skins
from utils.functions.gameObject import Personaje, Arco, Pelota, Contador
from utils.functions.functionMenu import show_menu_seleccion, show_ranking, show_menu_juego
from utils.functions.functionRegister import login_usuario, registro_usuario
from config import (
    BLANCO, WIDTH, HEIGHT, ventana, ROJO,
    menu_opciones, opcion, fondoResponsive,
    fuente_chica, fuente, clock, FPS,
    duracion_partido, link_rect, menu_juego
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
menuGame = False
usuario_actual = None
goles_bot = 0
goles_jugador = 0
last_event_time = 0
fecha = datetime.now().strftime("%Y-%m-%d")
ranking = False



# -------------------
# LOOP PRINCIPAL
# -------------------
execute = False
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cursor = pygame.SYSTEM_CURSOR_ARROW  # cursor por defecto
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        if link_rect.collidepoint(mouse_x, mouse_y):
            webbrowser.open("https://github.com/Agustincito1")

        # Menú principal
        if menu:
            opcion
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
                            execute = True
                            # Ejecutar acción correspondiente
                            
                    # Clic sobre el link de GitHub

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion = (opcion - 1) % len(menu_opciones)
                if event.key == pygame.K_DOWN:
                    opcion = (opcion + 1) % len(menu_opciones)
                if event.key == pygame.K_RETURN:
                    execute = True
            
            
            if execute:
                if opcion == 0:
                    usuario_actual = login_usuario()
                    if usuario_actual:
                        menu = False
                        menuGame = True
                    execute = False
                    continue
                elif opcion == 1:
                    valorRegistro = registro_usuario()
                    execute = False

                    continue
                elif opcion == 2:
                    pygame.quit()


        if menuGame:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                right_start = int(WIDTH * 0.55)
                spacing = 60
                start_y = HEIGHT // 3
                for i, texto_opcion in enumerate(menu_juego):
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
                    for i, texto_opcion in enumerate(menu_juego):
                        opcion_render = fuente_chica.render(texto_opcion, True, BLANCO)
                        opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
                        opcion_y = start_y + i * spacing
                        rect = pygame.Rect(opcion_x, opcion_y, opcion_render.get_width(), opcion_render.get_height())

                        if rect.collidepoint(mouse_x, mouse_y):
                            opcion = i
                            execute = True
                            # Ejecutar acción correspondiente
                           

                    # Clic sobre el link de GitHub
                    if link_rect.collidepoint(mouse_x, mouse_y):
                        webbrowser.open("https://github.com/Agustincito1")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opcion = (opcion - 1) % len(menu_juego)
                if event.key == pygame.K_DOWN:
                    opcion = (opcion + 1) % len(menu_juego)
                if event.key == pygame.K_RETURN:
                    execute = True
                    
            if execute:
                if opcion == 0:
                    menuGame = False
                    execute = False
                    continue
                elif opcion == 1:
                    show_ranking(usuario_actual)
                    execute = False
                    continue
                elif opcion == 2:
                    name = SacarUsuario(usuario_actual)
                    show_preguntas(name)
                    execute = False
                elif opcion == 3:
                    name = SacarUsuario(usuario_actual)
                    mostrar_mercado_skins(name)
                    execute = False
                elif opcion == 4:
                    pygame.quit()
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

    if menuGame:

        right_start = int(WIDTH * 0.55)
        spacing = 60
        start_y = HEIGHT // 3
        for i, texto_opcion in enumerate(menu_juego):
            opcion_render = fuente_chica.render(texto_opcion, True, BLANCO)
            opcion_x = right_start + ((WIDTH - right_start) - opcion_render.get_width()) // 2
            opcion_y = start_y + i * spacing
            rect = pygame.Rect(opcion_x, opcion_y, opcion_render.get_width(), opcion_render.get_height())
            if rect.collidepoint(mouse_x, mouse_y):
                cursor = pygame.SYSTEM_CURSOR_HAND

        if link_rect.collidepoint(mouse_x, mouse_y):
            cursor = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor)
        
        pygame.mouse.set_cursor(cursor)
        show_menu_juego(opcion, mouse_x, mouse_y, usuario_actual)

        pygame.display.flip()
        continue

        
    # =======================
    # RANKING
    # =======================
    if ranking:
        print("ranking en proceso")
        show_ranking()
        continue

    menuGame = gameShow(usuario_actual, goles_bot, goles_jugador, last_event_time,
                    jugador, bot, pelota, contador, arco_izquierdo, arco_derecho)

    clock.tick(FPS)
