
import sys
from iaMens import generar_mensaje
from config import WIDTH, HEIGHT, duracion_partido, fuente, fuente_chica, fondoResponsive, BLANCO, ROJO, FPS, ventana, clock
from utils.functions.functionRegister import registrar_resultado
from utils.functions.registroColisiones import registroContinuo
from conn import get_connection
from utils.functions.gameObject import arcoDibujo
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
    bot.bot_rect.x = WIDTH - 200
    bot.bot_rect.y = HEIGHT - 50
    jugador.player_rect.x = 100
    jugador.player_rect.y = HEIGHT - 50
    contador.tiempo_restante = duracion_partido
    contador.reset(pygame.time.get_ticks())
    contador.stop(pygame.time.get_ticks())


def game_over_screen(resultado, goles_jugador, goles_bot, contador):
    
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

                    if seleccion == 0:
                        return "replay"  # Jugar de nuevo
                    else:
                        
                        return "menu"    # Volver al menú
        
        clock.tick(FPS)





# Mostrar juego y detectar goles
def gameShow(id_usuario, goles_bot, goles_jugador, last_event_time, jugador, bot, pelota, contador, arco_izquierdo, arco_derecho):
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
   
        accion = game_over_screen(resultado, goles_jugador, goles_bot, contador)

        if accion == "menu":
            return True  # Volver al menú
            
        else:
            resetGame(goles_bot, goles_jugador, contador, jugador, bot, pelota)
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


    if eventVar and (now - last_event_time) > 5000:  # Evita mensajes muy seguidos
        last_event_time = now
    
        import threading

        def registrar_mensaje_sync(id_usuario, eventVar):

            mensaje = asyncio.run(generar_mensaje(SacarUsuario(id_usuario), str(eventVar[0][0])))

            try:
                conn = get_connection()  # tu función importada
                cursor = conn.cursor()
                sql = "INSERT INTO mensaje (mensaje) VALUES (%s)"
                cursor.execute(sql, (mensaje,))
                conn.commit()
                print("✅ Mensaje registrado en DB:", mensaje)
            except Exception as e:
                print("❌ Error al registrar mensaje:", e)
            finally:
                cursor.close()
                conn.close()

        threading.Thread(
            target=registrar_mensaje_sync,
            args=(id_usuario, eventVar),
            daemon=True
        ).start()
    
    pygame.display.flip()
