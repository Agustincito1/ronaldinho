##./utils/regist/juegos_diarios.txt

import openai
import os
import re
import pygame
import sys
import datetime
import json
from config import *

openai.api_key = "DRNY_MbPrGlC6EIdQfi8njlZyl2ui5V3jgsOrSiWFX4"
openai.api_base = "https://api.poe.com/v1"

ARCHIVO_DIARIO = "./utils/regist/juegos_diarios.txt"
LIMITE_PREGUNTAS = 3
USUARIO_ACTUAL = "usuario_demo_123"

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


def obtener_datos_diarios():
    datos = {}
    ultimo_id = 0
    if not os.path.exists(ARCHIVO_DIARIO):
        return datos, ultimo_id
    try:
        with open(ARCHIVO_DIARIO, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        # --- CAMBIO AQUÍ: LEEMOS 4 CAMPOS ---
                        campos = line.strip().split(',')
                        if len(campos) == 4:
                            registro_id, usuario, fecha, conteo = campos
                            datos[usuario] = {"id": int(registro_id), "fecha": fecha, "conteo": int(conteo)}
                            ultimo_id = max(ultimo_id, int(registro_id))
                    except ValueError:
                        continue 
        return datos, ultimo_id
    except IOError:
        return datos, ultimo_id

def guardar_datos_diarios(datos):
    try:
        with open(ARCHIVO_DIARIO, 'w') as f:
            for usuario, registro in datos.items():
                # --- CAMBIO AQUÍ: ESCRIBIMOS EL ID AL PRINCIPIO ---
                linea = f"{registro['id']},{usuario},{registro['fecha']},{registro['conteo']}\n"
                f.write(linea)
    except IOError as e:
        print(f"❌ Error al guardar el archivo diario: {e}")

def verificar_limite_diario(usuario):
    hoy = datetime.date.today().isoformat()
    datos_diarios, ultimo_id = obtener_datos_diarios()

    if usuario not in datos_diarios:
        # Asignamos un nuevo ID
        nuevo_id = ultimo_id + 1
        datos_diarios[usuario] = {"id": nuevo_id, "fecha": hoy, "conteo": 0}
        guardar_datos_diarios(datos_diarios)
        return True

    registro_usuario = datos_diarios[usuario]
    
    if registro_usuario["fecha"] == hoy:
        return registro_usuario["conteo"] < LIMITE_PREGUNTAS
    else:
        # Reiniciamos la fecha, el ID se mantiene
        registro_usuario["fecha"] = hoy
        registro_usuario["conteo"] = 0
        guardar_datos_diarios(datos_diarios)
        return True

def incrementar_conteo_diario(usuario):
    hoy = datetime.date.today().isoformat()
    datos_diarios, ultimo_id = obtener_datos_diarios()
    
    # Manejo del caso donde el usuario no existe (debería ser capturado por verificar_limite_diario)
    if usuario not in datos_diarios:
        nuevo_id = ultimo_id + 1
        datos_diarios[usuario] = {"id": nuevo_id, "fecha": hoy, "conteo": 1}
    
    # Incremento normal
    elif datos_diarios[usuario]["fecha"] == hoy:
        datos_diarios[usuario]["conteo"] += 1
    # Caso donde jugó antes, pero no se hizo verificación de límite al inicio del día
    else:
        datos_diarios[usuario]["fecha"] = hoy
        datos_diarios[usuario]["conteo"] = 1

    guardar_datos_diarios(datos_diarios)
    return datos_diarios[usuario]["conteo"]


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


def verificar_respuesta(pregunta, opciones, respuesta_usuario):
    prompt = f"Pregunta: {pregunta}\nOpciones: {opciones}\nRespuesta del usuario: {respuesta_usuario}\nEvalúa si la respuesta del usuario es correcta o incorrecta.\nSi es correcta, **SOLO RESPONDE EL NÚMERO 1**.\nSi es incorrecta, **SOLO RESPONDE EL NÚMERO 0**.\nNO AÑADAS NINGÚN OTRO TEXTO, EXPLICACIÓN O CARACTER ADICIONAL."
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


class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_base = color_base
        self.color_hover = color_hover
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

def mostrar_bloqueo():
    ventana.fill(COLOR_FONDO)
    
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
        


def show_preguntas(usuario):
    if not verificar_limite_diario(usuario):
        mostrar_bloqueo()
        return

    estado_juego = "CARGANDO"
    pregunta_actual = None
    opciones_botones = []
    mensaje_resultado = ""
    color_resultado = NEGRO
    
    datos_diarios, _ = obtener_datos_diarios()
    conteo_actual = datos_diarios.get(usuario, {}).get("conteo", 0)

    def cargar_nueva_pregunta():
        nonlocal estado_juego, pregunta_actual, opciones_botones, mensaje_resultado, color_resultado
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
                            respuesta_elegida
                        )

                        if resultado == 1:
                            mensaje_resultado = "✅ ¡CORRECTO! Driblaste a la ignorancia."
                            color_resultado = COLOR_CORRECTO
                        elif resultado == 0:
                            mensaje_resultado = "❌ INCORRECTO. Sigue practicando."
                            color_resultado = COLOR_INCORRECTO
                        else:
                            mensaje_resultado = "⚠️ Error al verificar la respuesta."
                            color_resultado = COLOR_TEXTO
                            
                        estado_juego = "RESULTADO"
                        break
            
            elif estado_juego == "RESULTADO" and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                conteo_actual = incrementar_conteo_diario(usuario) 
                
                if conteo_actual >= LIMITE_PREGUNTAS:
                    mostrar_bloqueo()
                    return 
                else:
                    cargar_nueva_pregunta()
            
            elif estado_juego == "ERROR" and evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                cargar_nueva_pregunta()
                
        ventana.fill(COLOR_FONDO)
        
        if logoMenuResponsive:
            ventana.blit(logoMenuResponsive, (10, 10))

        texto_conteo = fuente_chica2.render(f"Preguntas Hoy: {conteo_actual}/{LIMITE_PREGUNTAS}", True, BLANCOG)
        ventana.blit(texto_conteo, (WIDTH - texto_conteo.get_width() - 20, 20))

        if estado_juego == "PREGUNTANDO":
            titulo = fuente.render("El Quiz Ambiental de Ronaldinho", True, COLOR_TEXTO)
            ventana.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 50))
            
            pregunta_rect = pygame.Rect(WIDTH * 0.1, 150, WIDTH * 0.8, 100)
            pygame.draw.rect(ventana, COLOR_PREGUNTA_FONDO, pregunta_rect, border_radius=5)
            pygame.draw.rect(ventana, COLOR_BOTON_HOVER, pregunta_rect, 3, border_radius=5) 
            
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
    show_preguntas(USUARIO_ACTUAL)