import sys
from config import WIDTH, HEIGHT, duracion_partido, fuente, fuente_chica, fondoResponsive, BLANCO, ROJO, FPS, ventana, clock, arcoImg, fuente_chica2,AZUL_OSCURO
from utils.functions.registroColisiones import registroContinuo,  registrar_resultado
from utils.functions.obc import ArchivoEventos, COLUMNAS_EVENTOS, RUTA_REGISTRO_EVENTOS

gestor_eventos = ArchivoEventos(
    COLUMNAS_EVENTOS, 
    RUTA_REGISTRO_EVENTOS, 
)

from utils.functions.othersFunction import fisicas
from conn import get_connection
import pygame
import threading
from utils.functions.othersFunction import SacarUsuario
import asyncio
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

pygame.init()
from datetime import datetime
fecha = datetime.now().strftime("%Y-%m-%d")

def resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota):
    goles_bot = 0
    goles_jugador = 0
    pelota.reset_pelota()
    bot.rect.x = WIDTH - 200
    bot.rect.y = HEIGHT - bot.rect.height
    jugador.rect.x = 100
    jugador.rect.y = HEIGHT - jugador.rect.height 
    contador.tiempo_restante = duracion_partido
    contador.reset(pygame.time.get_ticks())
    contador.stop(pygame.time.get_ticks())


try:
    _arco_img_base = pygame.image.load('./utils/imgs/arcos.png').convert_alpha() # Nombre de archivo de tu imagen de portería
    # Escalar la imagen del arco si es necesario. Ajusta el tamaño según tu juego.
    _arco_w, _arco_h = 200, 150 # Ejemplo de tamaño, ajusta según sea necesario
    _arco_img_base = pygame.transform.scale(_arco_img_base, (_arco_w, _arco_h))
except pygame.error as e:
    print(f"Error al cargar la imagen del arco: {e}")
    sys.exit()
ARCO_Y_POS = HEIGHT - _arco_h 
arco_img_original = _arco_img_base
arco_img_reflejada = pygame.transform.flip(_arco_img_base, True, False)
arco_izquierdo_rect = arco_img_original.get_rect(topleft=(0, ARCO_Y_POS))# Ajusta Y si quieres que estén más abajo
arco_derecho_rect =  arco_img_reflejada.get_rect(topright=(WIDTH, ARCO_Y_POS)) # Ajusta Y si quieres que estén más abajo
def game_over_screen(resultado, goles_jugador, goles_bot, contador):
    opciones = ["Jugar de nuevo", "Volver al menú principal"]
    seleccion = 0
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Fondo del juego
        ventana.blit(fondoResponsive, (0, 0))

        # Capa semitransparente azul oscuro
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(AZUL_OSCURO)
        overlay.set_alpha(180)
        ventana.blit(overlay, (0, 0))

        # Título con sombra
        titulo = fuente.render(f"¡{resultado}!", True, BLANCO)
        sombra = fuente.render(f"¡{resultado}!", True, (0, 0, 0))
        ventana.blit(sombra, ((WIDTH - titulo.get_width()) // 2 + 3, HEIGHT // 4 + 3))
        ventana.blit(titulo, ((WIDTH - titulo.get_width()) // 2, HEIGHT // 4))

        # Marcador de goles
        marcador = fuente_chica.render(f"{goles_jugador} - {goles_bot}", True, BLANCO)
        ventana.blit(marcador, ((WIDTH - marcador.get_width()) // 2, HEIGHT // 4 + 70))

        opcion_rects = []
        for i, texto in enumerate(opciones):
            # Definir rectángulo del botón
            rect_x = WIDTH // 2 - 150
            rect_y = HEIGHT // 2 + i * 80
            rect_w = 300
            rect_h = 50
            rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
            opcion_rects.append(rect)

            # Hover con el mouse
            if rect.collidepoint(mouse_pos):
                color_fondo = BLANCO
                color_texto = AZUL_OSCURO
                seleccion = i
            else:
                color_fondo = (0, 0, 0, 0)
                color_texto = BLANCO

            # Dibujar botón
            pygame.draw.rect(ventana, color_fondo, rect, border_radius=15)
            pygame.draw.rect(ventana, BLANCO, rect, 2, border_radius=15)

            # Texto centrado en el botón
            texto_render = fuente_chica.render(texto, True, color_texto)
            ventana.blit(texto_render, texto_render.get_rect(center=rect.center))

        # Indicador sobre la opción seleccionada
        indicador_y = HEIGHT // 2 + seleccion * 80 - 10
        pygame.draw.rect(ventana, BLANCO, (WIDTH // 2 - 50, indicador_y, 100, 3), border_radius=2)

        pygame.display.flip()

        # Manejo de eventos
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
                    return "replay" if seleccion == 0 else "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(opcion_rects):
                        if rect.collidepoint(mouse_pos):
                            return "replay" if i == 0 else "menu"

        clock.tick(FPS)


def pause_menu():
    opciones = ["Continuar", "Volver al menú principal"]
    seleccion = 0
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Fondo del juego
        ventana.blit(fondoResponsive, (0, 0))

        # Capa semitransparente azul oscuro
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill(AZUL_OSCURO)
        overlay.set_alpha(180)
        ventana.blit(overlay, (0, 0))

        # Título con sombra
        titulo = fuente.render("|| PAUSA", True, BLANCO)
        sombra = fuente.render("|| PAUSA", True, (0, 0, 0))
        ventana.blit(sombra, ((WIDTH - titulo.get_width()) // 2 + 3, HEIGHT // 4 + 3))
        ventana.blit(titulo, ((WIDTH - titulo.get_width()) // 2, HEIGHT // 4))

        opcion_rects = []
        for i, texto in enumerate(opciones):
            # Hover
            rect_x = WIDTH // 2 - 150
            rect_y = HEIGHT // 2 + i * 80
            rect_w = 300
            rect_h = 50
            rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
            opcion_rects.append(rect)

            if rect.collidepoint(mouse_pos):
                color_fondo = BLANCO
                color_texto = AZUL_OSCURO
                seleccion = i
            else:
                color_fondo = (0, 0, 0, 0)
                color_texto = BLANCO

            # Fondo del botón
            pygame.draw.rect(ventana, color_fondo, rect, border_radius=15)
            pygame.draw.rect(ventana, BLANCO, rect, 2, border_radius=15)

            # Texto centrado
            texto_render = fuente_chica.render(texto, True, color_texto)
            ventana.blit(texto_render, texto_render.get_rect(center=rect.center))

        # Indicador pequeño (barra blanca arriba del botón seleccionado)
        indicador_y = HEIGHT // 2 + seleccion * 80 - 10
        pygame.draw.rect(ventana, BLANCO, (WIDTH // 2 - 50, indicador_y, 100, 3), border_radius=2)

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
                elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    return "continue"
                elif event.key == pygame.K_RETURN:
                    return "continue" if seleccion == 0 else "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(opcion_rects):
                        if rect.collidepoint(mouse_pos):
                            return "continue" if i == 0 else "menu"

        clock.tick(FPS)


def gameShow(id_usuario, goles_bot, goles_jugador, last_event_time, jugador, bot, pelota, contador, arco_izquierdo, arco_derecho):
    gameStart = True
    pelota.pelota_rect.x = WIDTH // 2
    pelota.pelota_rect.y = HEIGHT - 100
    pelota.pelota_speed_x = 0
    pelota.pelota_speed_y = 0
    paused = False

    while gameStart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota)
                        return True
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        contador.stop(pygame.time.get_ticks())
                    else:
                        contador.resume(pygame.time.get_ticks())

        keys = pygame.key.get_pressed()
        
        if not paused:
            jugador.mover(keys)
            jugador.update() 
            bot.mover_bot(pelota)
            bot.update()
            fisicas(jugador, bot, pelota, keys) 
            pelota.update()
            
            colision_con_jugador = pelota.check_colision(jugador, "jugador")
            pelota_controlable = (abs(pelota.pelota_speed_x) < 5.0) and (abs(pelota.pelota_speed_y) < 5.0)
            
            if colision_con_jugador == "jugador":
                es_patada = keys[pygame.K_SPACE]
                pelota.manejar_impacto(jugador, es_patada)
                
            colision_con_bot = pelota.check_colision(bot, "bot") 
            if colision_con_bot == "bot":
                pelota.manejar_impacto(bot, es_patada=True)

            pelota.update() 
            
            tiempo_actual = pygame.time.get_ticks()
            contador.resume(tiempo_actual)
            contador.update(tiempo_actual)
            
            if contador.tiempo_restante <= 0:
                ventana.blit(fondoResponsive, (0, 0))
                if goles_jugador > goles_bot:
                    resultado = "Victoria del Jugador"
                    registrar_resultado(id_usuario, "W")
                elif goles_bot > goles_jugador:
                    resultado = "Victoria del Bot"
                    registrar_resultado(id_usuario, "L")
                else:
                    resultado = "Empate"
                    registrar_resultado(id_usuario, "N")
                
                accion = game_over_screen(resultado, goles_jugador, goles_bot, contador)

                if accion == "menu":
                    return True
                else:
                    resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota)
                    return False
            
                        
           
            ventana.blit(fondoResponsive, (0, 0))
            ventana.blit(pelota.pelota_img, pelota.pelota_rect)
            arco_izquierdo.draw(ventana)
            arco_derecho.draw(ventana)
            ventana.blit(jugador.image, jugador.rect)
            ventana.blit(bot.image, bot.rect)

            if jugador.rect.colliderect(arco_izquierdo.rect):
                jugador.rect.left = arco_izquierdo.rect.right

            if jugador.rect.colliderect(arco_derecho.rect):
                jugador.rect.right = arco_derecho.rect.left

            if bot.rect.colliderect(arco_izquierdo.rect):
                bot.rect.left = arco_izquierdo.rect.right

            if bot.rect.colliderect(arco_derecho.rect):
                bot.rect.right = arco_derecho.rect.left

            MARCADOR_W, MARCADOR_H = 150, 60
            MARCADOR_X = (WIDTH - MARCADOR_W) // 2
            MARCADOR_Y = 20
            pygame.draw.rect(ventana, (10, 20, 30), (MARCADOR_X, MARCADOR_Y, MARCADOR_W, MARCADOR_H), border_radius=10)

            marcador_texto = fuente.render(f"{goles_jugador} - {goles_bot}", True, BLANCO)
            ventana.blit(marcador_texto, 
                         (MARCADOR_X + (MARCADOR_W - marcador_texto.get_width()) // 2, 
                          MARCADOR_Y + (MARCADOR_H - marcador_texto.get_height()) // 2))

            CONTADOR_W, CONTADOR_H = 100, 40
            CONTADOR_X = (WIDTH - CONTADOR_W) // 2
            CONTADOR_Y = MARCADOR_Y + MARCADOR_H + 5 
            pygame.draw.rect(ventana, (10, 20, 30), (CONTADOR_X, CONTADOR_Y, CONTADOR_W, CONTADOR_H), border_radius=10)

            ventana.blit(contador.text, 
                         (CONTADOR_X + (CONTADOR_W - contador.text.get_width()) // 2, 
                          CONTADOR_Y + (CONTADOR_H - contador.text.get_height()) // 2))

            isGol = False
            mensaje_gol_texto = ""
            
            # ⚽️ CORRECCIÓN: USANDO EL RECTÁNGULO DEL ÁREA DE GOL
            if arco_derecho.goal_area_rect.colliderect(pelota.pelota_rect):
                isGol = True
                goles_jugador += 1
                contador.stop(pygame.time.get_ticks())
                mensaje_gol_texto = "¡JUGADOR ANOTÓ!"
                
            elif arco_izquierdo.goal_area_rect.colliderect(pelota.pelota_rect):
                isGol = True
                goles_bot += 1
                contador.stop(pygame.time.get_ticks())
                mensaje_gol_texto = "¡BOT ANOTÓ!"

            if isGol:
                ALERTA_W, ALERTA_H = 600, 80 
                ALERTA_X = (WIDTH - ALERTA_W) // 2
                ALERTA_Y = CONTADOR_Y + CONTADOR_H + 10 
                
                pygame.draw.rect(ventana, (30, 30, 30), (ALERTA_X, ALERTA_Y, ALERTA_W, ALERTA_H), border_radius=15)
                pygame.draw.rect(ventana, ROJO, (ALERTA_X+5, ALERTA_Y+5, ALERTA_W-10, ALERTA_H-10), 5, border_radius=15)
                
                mensaje_gol = fuente_chica.render(mensaje_gol_texto, True, BLANCO) 
                ventana.blit(mensaje_gol, 
                             (ALERTA_X + (ALERTA_W - mensaje_gol.get_width()) // 2, 
                              ALERTA_Y + (ALERTA_H - mensaje_gol.get_height()) // 2))

                pygame.display.flip()
                pygame.time.wait(1500)
                
                pelota.pelota_rect.x = WIDTH // 2
                pelota.pelota_rect.y = HEIGHT - 100
                pelota.pelota_speed_x = 0
                pelota.pelota_speed_y = 0
                jugador.rect.x = 100
                jugador.rect.y = HEIGHT - jugador.rect.height
                bot.rect.x = WIDTH - 200
                bot.rect.y = HEIGHT - bot.rect.height
                contador.resume(pygame.time.get_ticks())

            eventVar = registroContinuo(gestor_eventos, jugador, id_usuario, pelota, fecha, bot, arco_derecho, arco_izquierdo)
            now = pygame.time.get_ticks()
            pygame.display.flip()
        
        else:
            accion = pause_menu() 
            if accion == "continue":
                paused = False
                contador.resume(pygame.time.get_ticks())
            elif accion == "menu":
                resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota)
                return True

        clock.tick(FPS)
