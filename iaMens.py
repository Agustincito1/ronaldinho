import openai
import os
import re
import pygame
import sys
import datetime
import json
from config import *
from utils.puntero.punteroObj import PunteroObj


# --- CONFIGURACIÓN DE ARCHIVOS Y API ---
openai.api_key = "DRNY_MbPrGlC6EIdQfi8njlZyl2ui5V3jgsOrSiWFX4"
openai.api_base = "https://api.poe.com/v1"
puntero = PunteroObj()
LIMITE_PREGUNTAS = 3
USUARIO_ACTUAL = 1

ROJO_PRINCIPAL = ROJO 
GRIS_CLARO_BG = BLANCOG
GRIS_OSCURO_BG = AZUL_OSCURO 
COLOR_FONDO = MENU_BG_COLOR 
COLOR_PREGUNTA_FONDO = AZUL_OSCURO 
COLOR_BOTON_BASE = BLANCOG 
COLOR_BOTON_HOVER = ROJO 
COLOR_TEXTO = BLANCO
COLOR_CORRECTO = (50, 200, 50) 
COLOR_INCORRECTO = (255, 50, 50) 
COLOR_PUNTUACION = (255, 215, 0)




def generar_mensaje(usuario):
    prompt = "Genera una pregunta sobre educación ambiental con 3 opciones. Devuélvelo exactamente en formato JSON con esta estructura: {\"pregunta\": \"texto de la pregunta\", \"opciones\": [\"opción A\", \"opción B\", \"opción C\"]} No escribas nada fuera del JSON."
    try:
        chat = openai.ChatCompletion.create(
            model="BotLX18X5TJQ9", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        mensaje = chat.choices[0].message["content"].strip()
        print("Respuesta de IA bruta:", mensaje) 
        
        match = re.search(r"\{.*\}", mensaje, re.DOTALL)
        if match:
            mensaje_json = match.group(0)
            data = json.loads(mensaje_json)
            return data
        else:
            print("⚠️ No se encontró JSON en el texto.")
            return None

    except Exception as e:
        print("❌ Error al comunicarse con la IA o al convertir a JSON:", e)
        return {
            "pregunta": "¿Error de conexión. Pulsa para reintentar o Salir.",
            "opciones": ["Reintentar", "Salir", "Reintentar"]
        }

from conn import get_connection

def verificar_respuesta(pregunta, opciones, respuesta_usuario, usuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Convertir lista de opciones a JSON
    opciones_json = json.dumps(opciones)

    query = """
        INSERT INTO mensaje (pregunta, opciones, respuesta, usuario)
        VALUES (%s, %s, %s, %s)
    """
    valores = (pregunta, opciones_json, respuesta_usuario, usuario)

    cursor.execute(query, valores)
    conn.commit()

    cursor.close()
    conn.close()

    # === Verificación con IA ===
    prompt = (
        f"Pregunta: {pregunta}\n"
        f"Opciones: {opciones}\n"
        f"Respuesta del usuario: {respuesta_usuario}\n"
        "Evalúa si la respuesta del usuario es correcta o incorrecta.\n"
        "Si es correcta, SOLO RESPONDE EL NÚMERO 1.\n"
        "Si es incorrecta, SOLO RESPONDE EL NÚMERO 0.\n"
        "NO AÑADAS NINGÚN OTRO TEXTO, EXPLICACIÓN O CARACTER ADICIONAL."
    )

    try:
        chat = openai.ChatCompletion.create(
            model="BotLX18X5TJQ9",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.0
        )

        mensaje = chat.choices[0].message["content"].strip()
        print(f"Respuesta de verificación de IA bruta: {mensaje}")

        match = re.search(r"[01]", mensaje)

        if match:
            return int(match.group(0))
        else:
            print("❌ No se pudo extraer 0 o 1 de la respuesta de la IA.")
            return -1

    except Exception as e:
        print("❌ Error al comunicarse con la IA para la verificación:", e)
        return -1
# --- CLASE BOTÓN (Existente) ---

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_base = color_base
        self.color_hover = color_hover
        # Se asume que 'fuente_chica' está definida en el scope global o en 'config.py'
        self.superficie_texto = fuente_chica.render(texto, True, NEGRO) 
        self.rect_texto = self.superficie_texto.get_rect(center=self.rect.center)
        self.color_actual = self.color_base
        self.accion = accion

    def dibujar(self, superficie):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_base
            
        pygame.draw.rect(superficie, self.color_actual, self.rect, border_radius=10)
        superficie.blit(self.superficie_texto, self.rect_texto)

    def verificar_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.accion
        return None

def envolver_texto(superficie, texto, fuente, color, rect_area):
    palabras = texto.split(' ')
    # Se asume que 'fuente_chica' está definida
    espacio = fuente.size(' ')[0] 
    max_ancho = rect_area.width
    x, y = rect_area.topleft
    
    linea_actual = ''
    for palabra in palabras:
        if fuente.size(linea_actual + palabra)[0] < max_ancho:
            linea_actual += palabra + ' '
        else:
            superficie_linea = fuente.render(linea_actual, True, color)
            superficie.blit(superficie_linea, (x, y))
            y += superficie_linea.get_height()
            linea_actual = palabra + ' '
            
    superficie_linea = fuente.render(linea_actual, True, color)
    superficie.blit(superficie_linea, (x, y))

# --- FUNCIÓN DE BLOQUEO/FINAL (Modificada para mostrar el total actual) ---

def mostrar_bloqueo(puntaje_ganado=None, puntaje_acumulado=None):
    ventana.fill(COLOR_FONDO)
    
    if puntaje_ganado is not None:
        # Modo: Fin de Juego
        mensaje1 = fuente.render("¡Sesión de Quiz Terminada!", True, COLOR_PUNTUACION)
        mensaje2 = fuente_chica.render(f"Puntos Ganados Hoy: {puntaje_ganado} monedas", True, COLOR_PUNTUACION)
        mensaje3 = fuente_chica.render(f"Tu Total Acumulado: {puntaje_acumulado} monedas", True, COLOR_TEXTO)
        mensaje4 = fuente_chica.render("Vuelve mañana para seguir acumulando.", True, COLOR_TEXTO)

        ventana.blit(mensaje1, (WIDTH // 2 - mensaje1.get_width() // 2, HEIGHT // 3 - 50))
        ventana.blit(mensaje2, (WIDTH // 2 - mensaje2.get_width() // 2, HEIGHT // 3 + 50))
        ventana.blit(mensaje3, (WIDTH // 2 - mensaje3.get_width() // 2, HEIGHT // 3 + 100))
        ventana.blit(mensaje4, (WIDTH // 2 - mensaje4.get_width() // 2, HEIGHT // 3 + 180))
    else:
        # Modo: Bloqueo por Límite
        mensaje1 = fuente.render("¡Límite Diario Alcanzado!", True, COLOR_INCORRECTO)
        mensaje2 = fuente_chica.render("Vuelve mañana para más preguntas de Ronaldinho.", True, COLOR_TEXTO)
        mensaje3 = fuente_chica.render("Presiona ESC o cierra la ventana.", True, COLOR_TEXTO)

        ventana.blit(mensaje1, (WIDTH // 2 - mensaje1.get_width() // 2, HEIGHT // 3))
        ventana.blit(mensaje2, (WIDTH // 2 - mensaje2.get_width() // 2, HEIGHT // 3 + 100))
        ventana.blit(mensaje3, (WIDTH // 2 - mensaje3.get_width() // 2, HEIGHT // 3 + 150))
    
    pygame.display.flip()

    bloqueado = True
    while bloqueado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                bloqueado = False
        clock.tick(FPS)
        
# --- BUCLE PRINCIPAL DEL JUEGO (Modificado) --- ver esto para que cuando el usuario no tenga datosse registre
def registrar_datos(usuario):
    hoy = datetime.date.today().isoformat()
    puntero.registrarPuntuaciones(usuario, 0)
    puntero.registrarJuegos(usuario, hoy, 0)

def show_preguntas(usuario):

    
    hoy = datetime.date.today().isoformat()
    # registrar_datos(usuario)

    if not puntero.validarDiario(int(usuario), hoy):
        mostrar_bloqueo()
        return

    estado_juego = "CARGANDO"
    pregunta_actual = None
    opciones_botones = []
    mensaje_resultado = ""
    color_resultado = NEGRO
    
    # Variables de puntuación
    respuestas_correctas = 0
    conteo_actual = puntero.validarDiario(int(usuario), hoy)
    
    # Obtener el puntaje total actual para mostrarlo en el HUD
    puntaje_acumulado = puntero.getPuntajeUser(int(usuario))


    def cargar_nueva_pregunta():
        nonlocal estado_juego, pregunta_actual, opciones_botones, mensaje_resultado, color_resultado
        
        # Verificar si el límite ya se alcanzó al inicio de la carga
        if int(conteo_actual) >= LIMITE_PREGUNTAS:
            manejar_fin_de_juego()
            return

        estado_juego = "CARGANDO"
        ventana.fill(COLOR_FONDO)
        texto_cargando = fuente_chica.render("Cargando pregunta de la IA...", True, COLOR_TEXTO)
        ventana.blit(texto_cargando, (WIDTH // 2 - texto_cargando.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        
        pregunta_data = generar_mensaje(1)
        if pregunta_data:
            pregunta_actual = pregunta_data
            opciones_botones = []
            estado_juego = "PREGUNTANDO"
            
            opciones = pregunta_actual["opciones"]
            y_inicio = HEIGHT // 2 + 50 
            alto_boton = 60
            separacion = 25
            ancho_boton = WIDTH * 0.7 
            
            for i, opcion in enumerate(opciones):
                x = WIDTH // 2 - (ancho_boton // 2)
                y = y_inicio + (alto_boton + separacion) * i
                opciones_botones.append(Boton(x, y, ancho_boton, alto_boton, opcion, COLOR_BOTON_BASE, COLOR_BOTON_HOVER, opcion))
        else:
            estado_juego = "ERROR"
            mensaje_resultado = "¡Error al obtener la pregunta! Revisa tu conexión/clave."
            color_resultado = COLOR_INCORRECTO
    
    def manejar_fin_de_juego():
        """Calcula el puntaje ganado y lo guarda, luego muestra el resultado."""
        nonlocal respuestas_correctas, puntaje_acumulado
        
        # Calcular puntaje ganado en esta sesión: respuestas_correctas * 10
        puntaje_ganado = respuestas_correctas * 10
        
        # Guardar el puntaje y obtener el total acumulado
        puntero.registrarPuntuaciones(int(usuario), puntaje_ganado)
        
        # Necesitamos recargar las puntuaciones para mostrar el total fina
        
        puntaje_acumulado_final = puntero.getPuntajeUser(int(usuario))
        mostrar_bloqueo(puntaje_ganado, puntaje_acumulado_final)
        return

    cargar_nueva_pregunta()

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if estado_juego == "PREGUNTANDO" and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicion_click = evento.pos
                for boton in opciones_botones:
                    respuesta_elegida = boton.verificar_click(posicion_click)
                    if respuesta_elegida:
                        print(f"Respuesta elegida: {respuesta_elegida}")
                        
                        resultado = verificar_respuesta(
                            pregunta_actual["pregunta"], 
                            pregunta_actual["opciones"], 
                            respuesta_elegida,
                            usuario
                        )

                        if resultado == 1:
                            mensaje_resultado = "✅ ¡CORRECTO! Driblaste a la ignorancia. (+10 Monedas)"
                            color_resultado = COLOR_CORRECTO
                            # Incrementar contador de respuestas correctas (cada una vale 10)
                            respuestas_correctas += 1
                        elif resultado == 0:
                            mensaje_resultado = "❌ INCORRECTO. Sigue practicando. (+0 Monedas)"
                            color_resultado = COLOR_INCORRECTO
                        else:
                            mensaje_resultado = "⚠️ Error al verificar la respuesta."
                            color_resultado = COLOR_TEXTO
                            
                        estado_juego = "RESULTADO"
                        break
            
            elif estado_juego == "RESULTADO" and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                # Se incrementa el conteo de juegos diarios
                conteo_actual = int(puntero.conteoDiario(int(usuario), hoy)) 
                
                if conteo_actual >= LIMITE_PREGUNTAS:
                    manejar_fin_de_juego() # Llama a la nueva función de fin de juego
                    return 
                else:
                    cargar_nueva_pregunta()
            
            elif estado_juego == "ERROR" and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                cargar_nueva_pregunta()
                
        # --- LÓGICA DE DIBUJO ---
        ventana.fill(COLOR_FONDO)
        
        # Asumiendo que 'logoMenuResponsive' está definido y configurado en 'config.py'
        if 'logoMenuResponsive' in globals() and logoMenuResponsive:
            ventana.blit(logoMenuResponsive, (10, 10))

        # HUD (Preguntas de hoy y Monedas Acumuladas)
        texto_conteo = fuente_chica2.render(f"Preguntas Hoy: {conteo_actual}/{LIMITE_PREGUNTAS}", True, BLANCOG)
        ventana.blit(texto_conteo, (WIDTH - texto_conteo.get_width() - 20, 20))
        
        # Muestra el total acumulado actual (solo se actualiza al inicio o al terminar la sesión)
        puntaje_actual_mostrar = puntero.getPuntajeUser(int(usuario))
        texto_monedas = fuente_chica2.render(f"Monedas: {puntaje_actual_mostrar}", True, COLOR_PUNTUACION)
        ventana.blit(texto_monedas, (WIDTH - texto_monedas.get_width() - 20, 50))

        if estado_juego == "PREGUNTANDO":
            # Asumiendo que 'fuente' está definida
            titulo = fuente.render("El Quiz Ambiental de Ronaldinho", True, COLOR_TEXTO)
            ventana.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
            
            pregunta_rect = pygame.Rect(WIDTH * 0.1, 150, WIDTH * 0.8, 100)
            pygame.draw.rect(ventana, COLOR_PREGUNTA_FONDO, pregunta_rect, border_radius=5)
            pygame.draw.rect(ventana, COLOR_BOTON_HOVER, pregunta_rect, 3, border_radius=5) 
            
            # Asumiendo que 'fuente_chica' está definida
            envolver_texto(ventana, pregunta_actual["pregunta"], fuente_chica, COLOR_TEXTO, pygame.Rect(pregunta_rect.x + 10, pregunta_rect.y + 10, pregunta_rect.width - 20, pregunta_rect.height - 20))
            
            for boton in opciones_botones:
                boton.dibujar(ventana)

        elif estado_juego == "RESULTADO":
            resultado_texto = fuente.render(mensaje_resultado, True, color_resultado)
            ventana.blit(resultado_texto, (WIDTH // 2 - resultado_texto.get_width() // 2, HEIGHT // 2 - 50))
            
            instruccion = fuente_chica.render("Pulsa ESPACIO para la siguiente...", True, COLOR_TEXTO)
            ventana.blit(instruccion, (WIDTH // 2 - instruccion.get_width() // 2, HEIGHT // 2 + 50))
            
        elif estado_juego == "ERROR":
            error_texto = fuente.render(mensaje_resultado, True, color_resultado)
            ventana.blit(error_texto, (WIDTH // 2 - error_texto.get_width() // 2, HEIGHT // 2 - 50))
            
            instruccion = fuente_chica.render("Pulsa ESPACIO para reintentar...", True, COLOR_TEXTO)
            ventana.blit(instruccion, (WIDTH // 2 - instruccion.get_width() // 2, HEIGHT // 2 + 50))


        pygame.display.flip()
        clock.tick(FPS)

    return

if __name__ == "__main__":
    pygame.init()
    try:
        WIDTH, HEIGHT = 800, 600
        FPS = 60
        ventana = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Quiz Ambiental Ronaldinho")
        clock = pygame.time.Clock()
        # Inicialización de fuentes (ejemplo)
        fuente = pygame.font.Font(None, 48)
        fuente_chica = pygame.font.Font(None, 30)
        fuente_chica2 = pygame.font.Font(None, 24)
        NEGRO = (0, 0, 0)
        BLANCOG = (240, 240, 240)
        
        # Variables placeholder para evitar errores si no están en config.py
        if 'logoMenuResponsive' not in globals(): logoMenuResponsive = None 
        if 'ROJO' not in globals(): ROJO = (255, 0, 0)
        if 'AZUL_OSCURO' not in globals(): AZUL_OSCURO = (10, 20, 40)
        if 'BLANCO' not in globals(): BLANCO = (255, 255, 255)
        if 'MENU_BG_COLOR' not in globals(): MENU_BG_COLOR = (40, 40, 60)

        show_preguntas(USUARIO_ACTUAL)
        pygame.quit()
        sys.exit()
    except NameError as e:
        print(f"Error: {e}. Asegúrate de que todas las variables globales (WIDTH, HEIGHT, fuentes, colores, etc.) estén correctamente definidas en 'config.py' o en el scope global.")
