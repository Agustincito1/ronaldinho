import pygame
import sys

from config import ventana, HEIGHT, WIDTH, NEGRO, fuente_chica, fuente_chica2, AZUL_OSCURO, BLANCOG, ROJO, fuente, clock, FPS

SKIN_COSTO = 300
MAX_SKINS_PERMITIDAS = 3
RUTA_PUNTAJE = "./utils/regist/puntuaciones_totales.txt"
RUTA_SKINS = "./utils/regist/skins_adquiridas.txt"

VERDE_COMPRA = (50, 200, 50)
VERDE_COMPRA_HOVER = (100, 255, 100)
ROJO_ERROR = (200, 50, 50)
ROJO = (255, 165, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

SKINS_DISPONIBLES = {
    'skin_roja': ('Skin Roja', './utils/imgs/pg.png'), 
    'skin_verde': ('Skin Verde', './utils/imgs/pg.png'),
    'skin_azul': ('Skin Azul', './utils/imgs/pg.png')
}

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None, fuente=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.accion = accion
        self.fuente = fuente if fuente is not None else pygame.font.Font(None, 35)
        self.superficie_texto = self.fuente.render(texto, True, NEGRO)
        self.rect_texto = self.superficie_texto.get_rect(center=self.rect.center)

    def dibujar(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        color_actual = self.color_hover if self.rect.collidepoint(mouse_pos) else self.color_base
        pygame.draw.rect(superficie, color_actual, self.rect, border_radius=10)
        superficie.blit(self.superficie_texto, self.rect_texto)

    def clic(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos) and self.accion:
            return self.accion()
        return None

def mostrar_mercado_skins(nombre_usuario):
    
    def _obtener_puntos_actuales(user):
        try:
            with open(RUTA_PUNTAJE, "r") as file:
                for line in file:
                    partes = line.strip().split(',')
                    if len(partes) >= 3 and partes[1].strip().lower() == user.lower():
                        return int(partes[2].strip())
            return 0 
        except:
            return 0

    def _actualizar_puntos_usuario(user, puntos_a_restar):
        try:
            with open(RUTA_PUNTAJE, "r") as file:
                lineas = file.readlines()
        except FileNotFoundError:
            return False, "Archivo de puntos no encontrado."

        nueva_lineas = []
        usuario_encontrado = False
        
        for linea in lineas:
            partes = linea.strip().split(',')
            if len(partes) >= 3 and partes[1].strip().lower() == user.lower():
                usuario_encontrado = True
                id_fila, nombre, puntos_str = partes[0], partes[1], partes[2]
                try:
                    puntos_actuales = int(puntos_str.strip())
                except ValueError: continue
                
                if puntos_actuales >= puntos_a_restar:
                    nuevos_puntos = puntos_actuales - puntos_a_restar
                    nueva_linea_usuario = f"{id_fila},{nombre},{nuevos_puntos}\n"
                    nueva_lineas.append(nueva_linea_usuario)
                else:
                    nueva_lineas.append(linea) 
                    return False, "Puntos insuficientes."
            else:
                nueva_lineas.append(linea)

        if not usuario_encontrado:
            return False, "Usuario no encontrado en puntajes."

        try:
            with open(RUTA_PUNTAJE, "w") as file:
                file.writelines(nueva_lineas)
            return True, "Puntos restados exitosamente."
        except Exception as e:
            return False, f"Error al escribir puntos: {e}"

    def _cargar_skins_usuario(user):
        try:
            with open(RUTA_SKINS, "r") as file:
                for line in file:
                    partes = line.strip().split(',')
                    if partes and partes[0].strip().lower() == user.lower():
                        return set(p.strip() for p in partes[1:])
            return set()
        except FileNotFoundError:
            with open(RUTA_SKINS, "w") as file: pass 
            return set()

    def _guardar_nueva_skin(user, nueva_skin_clave):
        skins_existentes = {} 

        try:
            with open(RUTA_SKINS, "r") as file:
                for line in file:
                    partes = line.strip().split(',')
                    if partes and partes[0]:
                        skins_existentes[partes[0].strip().lower()] = list(set(p.strip() for p in partes[1:]))
        except FileNotFoundError:
            pass 

        if user.lower() in skins_existentes:
            skins_existentes[user.lower()].append(nueva_skin_clave)
        else:
            skins_existentes[user.lower()] = [nueva_skin_clave]
            
        nueva_lineas_a_escribir = []
        for user_key, skins_list in skins_existentes.items():
            skins_unicas = list(set(skins_list)) 
            nueva_linea_a_escribir = user_key + ',' + ','.join(skins_unicas) + '\n'
            nueva_lineas_a_escribir.append(nueva_linea_a_escribir)

        try:
            with open(RUTA_SKINS, "w") as file:
                file.writelines(nueva_lineas_a_escribir)
            return True
        except Exception as e:
            return False

    def _intentar_comprar_skin(user, clave_skin, costo):
        skins_adquiridas = _cargar_skins_usuario(user)

        if clave_skin in skins_adquiridas:
            return False, "Error: ¡Ya tienes esta skin!"
            
        puntos_usuario = _obtener_puntos_actuales(user)
        if puntos_usuario < costo:
             return False, f"Puntos insuficientes. Necesitas {costo} Puntos."

        exito_puntos, mensaje_puntos = _actualizar_puntos_usuario(user, costo)
        
        if exito_puntos:
            exito_guardar = _guardar_nueva_skin(user, clave_skin)
            
            if exito_guardar:
                return True, f"¡Compra exitosa! Se restaron {costo} Puntos."
            else:
                return False, "Error CRÍTICO: No se pudo guardar la skin."
        else:
            return False, mensaje_puntos

    def _dibujar_texto_centrado(superficie, texto, fuente, color, y):
        texto_render = fuente.render(texto, True, color)
        rect_texto = texto_render.get_rect(center=(WIDTH // 2, y))
        superficie.blit(texto_render, rect_texto)

    total_ancho = MAX_SKINS_PERMITIDAS * 200 + (MAX_SKINS_PERMITIDAS - 1) * 50
    start_x = (WIDTH - total_ancho) // 2
    mensaje_estado = ""
    color_mensaje = BLANCO
    
    def _crear_botones_skins(skins_adquiridas):
        nuevos_botones = []
        skins_claves = list(SKINS_DISPONIBLES.keys())
        
        for i, clave_skin in enumerate(skins_claves[:MAX_SKINS_PERMITIDAS]):
            x = start_x + i * 250
            y = HEIGHT // 2 + 50
            
            es_adquirida = clave_skin in skins_adquiridas
            
            if es_adquirida:
                texto_boton = "Adquirida"
                color_b, color_h, accion = BLANCOG, BLANCOG, None
            else:
                texto_boton = f"Comprar ({SKIN_COSTO} P)"
                color_b, color_h = VERDE_COMPRA, VERDE_COMPRA_HOVER
                
                def generar_accion(cs):
                    return lambda: _intentar_comprar_skin(nombre_usuario, cs, SKIN_COSTO)
                accion = generar_accion(clave_skin)

            # Usamos fuente_chica que se asume global
            boton = Boton(x, y, 200, 50, texto_boton, color_b, color_h, accion, fuente=fuente_chica) 
            nuevos_botones.append((clave_skin, boton))
            
        return nuevos_botones

    skins_adquiridas_inicial = _cargar_skins_usuario(nombre_usuario)
    botones_skins = _crear_botones_skins(skins_adquiridas_inicial)

    # Usamos fuente_chica que se asume global
    boton_volver = Boton(50, HEIGHT - 80, 150, 50, "Volver", ROJO, (255, 100, 100), fuente=fuente_chica)

    ejecutando = True
    while ejecutando:
        
        puntos_usuario = _obtener_puntos_actuales(nombre_usuario)
        skins_adquiridas = _cargar_skins_usuario(nombre_usuario)
        
        if any(clave not in [b[0] for b in botones_skins if b[1].texto == "Adquirida"] for clave in skins_adquiridas):
             botones_skins = _crear_botones_skins(skins_adquiridas)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if boton_volver.clic(evento):
                ejecutando = False
            
            for clave_skin, boton in botones_skins:
                resultado_accion = boton.clic(evento)
                if resultado_accion:
                    exito, msg = resultado_accion
                    mensaje_estado = msg
                    color_mensaje = VERDE_COMPRA if exito else ROJO_ERROR
                    if exito:
                        botones_skins = _crear_botones_skins(_cargar_skins_usuario(nombre_usuario))


        ventana.fill(AZUL_OSCURO) 
        
        _dibujar_texto_centrado(ventana, "MERCADO DE SKINS", fuente, ROJO, 50)
        
        puntos_texto = f"Tus Puntos: {puntos_usuario}"
        _dibujar_texto_centrado(ventana, puntos_texto, fuente_chica, BLANCO, 120)
        
        y_base_img = HEIGHT // 2 - 150
        
        for clave_skin, boton in botones_skins:
            x_img = boton.rect.centerx
            
            nombre_skin_render = fuente_chica2.render(SKINS_DISPONIBLES[clave_skin][0], True, BLANCO)
            nombre_skin_rect = nombre_skin_render.get_rect(center=(x_img, y_base_img + 30))
            ventana.blit(nombre_skin_render, nombre_skin_rect)
            
            try:
                ruta_img = SKINS_DISPONIBLES[clave_skin][1]
                img_skin = pygame.image.load(ruta_img).convert_alpha()
                img_skin = pygame.transform.scale(img_skin, (150, 150))
                
                img_skin_rect = img_skin.get_rect(center=(x_img, y_base_img + 120))
                ventana.blit(img_skin, img_skin_rect)
                
            except pygame.error:
                placeholder_rect = pygame.Rect(x_img - 75, y_base_img + 45, 150, 150)
                color_placeholder = (150, 150, 150) if clave_skin in skins_adquiridas else ROJO_ERROR
                pygame.draw.rect(ventana, color_placeholder, placeholder_rect)
                texto_ph = fuente_chica2.render("SIN IMAGEN", True, NEGRO)
                rect_ph = texto_ph.get_rect(center=(x_img, y_base_img + 120))
                ventana.blit(texto_ph, rect_ph)
            
            boton.dibujar(ventana)

        _dibujar_texto_centrado(ventana, mensaje_estado, fuente_chica, color_mensaje, HEIGHT - 150)
        
        boton_volver.dibujar(ventana)
        
        pygame.display.flip()
        clock.tick(FPS)
        
    return