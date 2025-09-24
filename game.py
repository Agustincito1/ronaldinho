# game.py

import pygame
import sys
import warnings
from datetime import datetime
from utils.functions.gameObject import Personaje, Arco, Pelota, Contador, arcoDibujo
from utils.functions.functionMenu import show_menu_seleccion, show_ranking
from utils.functions.functionRegister import login_usuario, registro_usuario, registrar_resultado
from utils.functions.registroColisiones import registroContinuo, resumenCol, evento_thread
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, menu_opciones, opcion, fondoResponsive, fuente_chica, fuente, clock, FPS, duracion_partido

from utils.functions.othersFunction import SacarUsuario 

# 🔇 Silencia warnings de pygame/pkg_resources
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

# Inicializamos pygame
pygame.init()

# Resumen inicial de colisiones
resumenCol()

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


# Funciones de físicas y reset
def fisicas(jugador, bot, pelota):
    if jugador.player_hitbox.colliderect(bot.bot_hitbox):
        empuje = 5
        if jugador.player_rect.centerx < bot.bot_rect.centerx:
            jugador.player_rect.x -= empuje
        else:
            jugador.player_rect.x += empuje
    jugador.update("user")
    bot.update("bot")
    pelota.update()
    pelota.colision(bot, "bot")
    pelota.colision(jugador, "")


def resetGame():
    global goles_bot, goles_jugador, contador
    goles_bot = 0
    goles_jugador = 0
    pelota.reset_pelota()
    bot.bot_rect.x = WIDTH - 200
    bot.bot_rect.y = HEIGHT - 50
    jugador.player_rect.x = 100
    jugador.player_rect.y = HEIGHT - 50
    contador.tiempo_restante = duracion_partido
    contador.reset(pygame.time.get_ticks())
    contador.stop(pygame.time.get_ticks())

def game_over_screen(resultado, goles_jugador, goles_bot):
    opciones = ["Jugar de nuevo", "Volver al menú principal"]
    seleccion = 0
    running = True
    
    while running:
        ventana.blit(fondoResponsive, (0, 0))
        
        # Mensaje principal
        mensaje = fuente.render(f"¡{resultado}!", True, BLANCO)
        ventana.blit(mensaje, ((WIDTH - mensaje.get_width()) // 2, HEIGHT // 4))
        
        # Marcador final
        marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, BLANCO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, HEIGHT // 4 + 50))
        
        # Mostrar opciones
        for i, texto in enumerate(opciones):
            color = ROJO if i == seleccion else BLANCO
            opcion_render = fuente_chica.render(texto, True, color)
            ventana.blit(opcion_render, ((WIDTH - opcion_render.get_width()) // 2, HEIGHT // 2 + i * 40))
        
        pygame.display.flip()
        
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    resetGame()
                    if seleccion == 0:
                        return "replay"  # Jugar de nuevo
                    else:
                        
                        return "menu"    # Volver al menú
        
        clock.tick(FPS)




# Mostrar juego y detectar goles
def gameShow(id_usuario):
    global goles_bot, goles_jugador, last_event_time

    isGol = False
    tiempo_actual = pygame.time.get_ticks()
    contador.resume(tiempo_actual)
    contador.update(tiempo_actual)
    
    # Fin del partido
    if contador.tiempo_restante <= 0:
        ventana.blit(fondoResponsive, (0, 0))
        if goles_jugador > goles_bot:
            mensaje = fuente.render("¡Jugador gana!", True, ROJO)
            registrar_resultado(id_usuario, "Ganó")
        elif goles_bot > goles_jugador:
            mensaje = fuente.render("¡Bot gana!", True, ROJO)
            registrar_resultado(id_usuario, "Perdió")
        else:
            mensaje = fuente.render("¡Empate!", True, ROJO)
            registrar_resultado(id_usuario, "Empató")
        ventana.blit(mensaje, ((WIDTH - mensaje.get_width()) // 2, HEIGHT // 2))
        marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, ROJO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, 30))
        pygame.display.flip()
        pygame.time.wait(2000)
    
    if contador.tiempo_restante <= 0:
        ventana.blit(fondoResponsive, (0, 0))
        if goles_jugador > goles_bot:
            resultado = "Jugador gana"
        elif goles_bot > goles_jugador:
            resultado = "Bot gana"
        else:
            resultado = "Empate"
   
        accion = game_over_screen(resultado, goles_jugador, goles_bot)
        if accion == "menu":

            return True  # Volver al menú
            
        else:
            resetGame()
            return False  # Seguir jugando

    # Dibujar escenario y objetos
    ventana.blit(fondoResponsive, (0, 0))
    ventana.blit(jugador.player_img, jugador.player_rect)
    ventana.blit(bot.bot_img, bot.bot_rect)
    ventana.blit(pelota.pelota_img, pelota.pelota_rect)
    arcoDibujo(ventana, arco_izquierdo.arco_izq_x, arco_izquierdo.arco_izq_y, direccion="izquierda")
    arcoDibujo(ventana, arco_izquierdo.arco_der_x, arco_izquierdo.arco_der_y, direccion="derecha")

    ventana.blit(contador.text, (WIDTH // 2 - contador.text.get_width() // 2, 70))
    marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, ROJO)
    ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, 30))

    # Detectar goles
    if arco_derecho.rect.colliderect(pelota.pelota_rect):
        isGol = True
        goles_jugador += 1
        contador.stop(pygame.time.get_ticks())
        ventana.blit(fondoResponsive, (0, 0))
        mensaje = fuente.render("Jugador anotó!", True, ROJO)
        ventana.blit(mensaje, ((WIDTH - mensaje.get_width()) // 2, HEIGHT // 2))
    elif arco_izquierdo.rect.colliderect(pelota.pelota_rect):
        isGol = True
        goles_bot += 1
        contador.stop(pygame.time.get_ticks())
        ventana.blit(fondoResponsive, (0, 0))
        mensaje = fuente.render("Bot anotó!", True, ROJO)
        ventana.blit(mensaje, ((WIDTH - mensaje.get_width()) // 2, HEIGHT // 2))

    if isGol:
        marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, ROJO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, 30))
        pygame.display.flip()
        pygame.time.wait(2000)
        pelota.pelota_rect.x = WIDTH // 2
        pelota.pelota_rect.y = HEIGHT - 100
        pelota.pelota_speed_x = 0
        pelota.pelota_speed_y = 0
        jugador.player_rect.x = 100
        jugador.player_rect.y = HEIGHT - jugador.player_rect.height
        bot.bot_rect.x = WIDTH - 200
        bot.bot_rect.y = HEIGHT - bot.bot_rect.height
        contador.resume(pygame.time.get_ticks())

    # Registrar eventos con IA
    eventVar = registroContinuo(jugador, id_usuario, pelota, fecha, bot, arco_derecho, arco_izquierdo)
    now = pygame.time.get_ticks()

    pygame.display.flip()


# -------------------
# LOOP PRINCIPAL
# -------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Menú principal
        if menu:
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
                        pygame.time.wait(2000)
                    elif opcion == 3:
                        pygame.quit()
                        sys.exit()
        else:  # juego en curso
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    resetGame()
                    menu = True
                    paused = False
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        contador.stop(pygame.time.get_ticks())
                    else:
                        contador.resume(pygame.time.get_ticks())

    if menu:
        show_menu_seleccion(opcion)
        continue

    if paused:
        ventana.blit(fondoResponsive, (0, 0))
        texto = fuente.render("|| Juego en Pausa", True, ROJO)
        ventana.blit(texto, ((WIDTH - texto.get_width()) // 2, HEIGHT // 2))
        marcador = fuente_chica.render(f"{goles_jugador}  -  {goles_bot}", True, ROJO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, 30))
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Movimiento y físicas
    keys = pygame.key.get_pressed()
    jugador.mover(keys)
    bot.mover_bot(pelota)
    fisicas(jugador, bot, pelota)
    menu = gameShow(usuario_actual)
    
    clock.tick(FPS)
