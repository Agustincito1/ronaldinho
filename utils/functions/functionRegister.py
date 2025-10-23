import pygame
import time 
import sys
from datetime import datetime
import os # Necesario para chequear rutas de archivo

# Asegúrate de que config.py contenga todas estas variables.
# Asumiendo que el  están en config
from config import (
    BLANCO, WIDTH, HEIGHT, ventana, ROJO, FPS, clock, fuente, 
    fondoMenuResponsive, fuente_chica, fuente_chica2, AZUL_OSCURO, 
    logoMenuResponsive, link_rect, link_text, REGISTRO_SIZE, 
    MAX_CARACTERES, LONGITUD_ID
)

pygame.init()

# --- Estilos de Apariencia (Mantenidos) ---
COLOR_CARD_BACKGROUND = (230, 230, 230)
COLOR_CAMPO_FONDO = (38, 43, 59)
COLOR_TITULO_Y_ETIQUETA = (50, 50, 50)
COLOR_BOTON = (43, 110, 219)
CARD_WIDTH_REL = 400
CARD_HEIGHT_REL = 400
BOTON_HEIGHT = 50
COLOR_FONDO_ERROR = (255, 100, 100)
COLOR_TEXTO_ERROR = (150, 0, 0)

# --- Variables Globales para Geometría (Mantenidas) ---
# ... (variables rect_form, rect_usuario, etc. declaradas globalmente) ...
rect_form = None
rect_usuario = None
rect_contrasena = None
rect_boton = None
TITULO_Y = None
ETIQUETA_USUARIO_Y = None
RECT_USUARIO_Y = None
ETIQUETA_CONTRASENA_Y = None
RECT_CONTRASENA_Y = None
RECT_BOTON_Y = None
RECT_ERROR = None

rect_form_r = None
rect_nombre_r = None
rect_contrasena_r = None
rect_boton_r = None
RECT_ERROR_R = None
TITULO_Y_R = None
RECT_NOMBRE_Y_R = None
RECT_CONTRASENA_Y_R = None
RECT_BOTON_Y_R = None

# --- Rutas de Archivo ---
RUTA_USUARIOS = "./utils/regist/usuarios.txt"


def calcular_geometria(current_width, current_height):
    """Calcula y actualiza todos los rectángulos de la interfaz de LOGIN."""
    global rect_form, rect_usuario, rect_contrasena, rect_boton, RECT_ERROR
    global TITULO_Y, ETIQUETA_USUARIO_Y, RECT_USUARIO_Y, ETIQUETA_CONTRASENA_Y, RECT_CONTRASENA_Y, RECT_BOTON_Y

    card_width = min(CARD_WIDTH_REL, current_width // 2)
    card_height = min(CARD_HEIGHT_REL, current_height - 100)

    CARD_X = int(current_width * 0.7) - (card_width // 2)
    CARD_Y = current_height // 2 - (card_height // 2)

    rect_form = pygame.Rect(CARD_X, CARD_Y, card_width, card_height)

    FIELD_WIDTH = int(card_width * 0.8)
    FIELD_HEIGHT = 40
    FIELD_X = CARD_X + (card_width - FIELD_WIDTH) // 2

    TITULO_Y = CARD_Y + 30
    ETIQUETA_USUARIO_Y = TITULO_Y + 70
    RECT_USUARIO_Y = ETIQUETA_USUARIO_Y + 25
    ETIQUETA_CONTRASENA_Y = RECT_USUARIO_Y + FIELD_HEIGHT + 20
    RECT_CONTRASENA_Y = ETIQUETA_CONTRASENA_Y + 25
    RECT_BOTON_Y = RECT_CONTRASENA_Y + FIELD_HEIGHT + 40
    ERROR_Y = RECT_BOTON_Y + BOTON_HEIGHT + 15

    rect_usuario = pygame.Rect(FIELD_X, RECT_USUARIO_Y, FIELD_WIDTH, FIELD_HEIGHT)
    rect_contrasena = pygame.Rect(FIELD_X, RECT_CONTRASENA_Y, FIELD_WIDTH, FIELD_HEIGHT)
    rect_boton = pygame.Rect(FIELD_X, RECT_BOTON_Y, FIELD_WIDTH, BOTON_HEIGHT)
    RECT_ERROR = pygame.Rect(FIELD_X, ERROR_Y, FIELD_WIDTH, 30)

# El resto de dibujar_login es correcto y se mantiene
def dibujar_login(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y):
    if rect_form is None:
        return
        
    ventana.blit(fondoMenuResponsive, (0, 0))

    # DIBUJAR LOGO (Simulado)
    if logoMenuResponsive:
        radio = min(current_width, current_height) // 5
        size = radio * 2
        
        # Simulación de imagen circular (simplificada)
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        logo_x = (current_width // 4) - (size // 2)
        logo_y = (current_height - size) // 2
        ventana.blit(circular_surface, (logo_x, logo_y))

    # 1. Panel de Login (Tarjeta)
    pygame.draw.rect(ventana, COLOR_CARD_BACKGROUND, rect_form, border_radius=10)

    # 2. Título "Jugar"
    texto_titulo = fuente.render("Jugar", True, COLOR_TITULO_Y_ETIQUETA)
    titulo_x = rect_form.x + (rect_form.width - texto_titulo.get_width()) // 2
    ventana.blit(texto_titulo, (titulo_x, TITULO_Y))

    # 3. Etiquetas de Campos
    etiqueta_usuario = fuente_chica.render("Usuario", True, COLOR_TITULO_Y_ETIQUETA)
    ventana.blit(etiqueta_usuario, (rect_usuario.x, ETIQUETA_USUARIO_Y)) 
    etiqueta_contrasena = fuente_chica.render("Contraseña", True, COLOR_TITULO_Y_ETIQUETA)
    ventana.blit(etiqueta_contrasena, (rect_contrasena.x, ETIQUETA_CONTRASENA_Y))

    # 4. Campos de Texto (Renderizados)
    
    # Campo Usuario
    texto_usuario = fuente_chica.render(nombre, True, BLANCO)
    pygame.draw.rect(ventana, COLOR_CAMPO_FONDO, rect_usuario, border_radius=5)
    text_y_usuario = rect_usuario.y + (rect_usuario.height - texto_usuario.get_height()) // 2
    ventana.blit(texto_usuario, (rect_usuario.x + 10, text_y_usuario))

    # Campo Contraseña
    texto_password = "*"*len(password)
    texto_password_render = fuente_chica.render(texto_password, True, BLANCO)
    pygame.draw.rect(ventana, COLOR_CAMPO_FONDO, rect_contrasena, border_radius=5)
    text_y_contrasena = rect_contrasena.y + (rect_contrasena.height - texto_password_render.get_height()) // 2
    ventana.blit(texto_password_render, (rect_contrasena.x + 10, text_y_contrasena))

    # 5. Botón
    pygame.draw.rect(ventana, COLOR_BOTON, rect_boton, border_radius=5)
    texto_boton = fuente_chica.render("Jugar", True, BLANCO)
    boton_text_x = rect_boton.x + (rect_boton.width - texto_boton.get_width()) // 2
    boton_text_y = rect_boton.y + (rect_boton.height - texto_boton.get_height()) // 2
    ventana.blit(texto_boton, (boton_text_x, boton_text_y))

    if error:
        # Dibujar un fondo para la alerta
        pygame.draw.rect(ventana, COLOR_FONDO_ERROR, RECT_ERROR, border_radius=5)
        
        # Renderizar el texto de error
        error_render = fuente_chica2.render(error, True, COLOR_TEXTO_ERROR)
        
        # Centrar el texto en el fondo del error
        error_x = RECT_ERROR.x + (RECT_ERROR.width - error_render.get_width()) // 2
        error_y = RECT_ERROR.y + (RECT_ERROR.height - error_render.get_height()) // 2
        
        ventana.blit(error_render, (error_x, error_y))


    if link_rect.collidepoint(mouse_x, mouse_y):
        link_color = (180, 220, 255)
        link_render = fuente_chica.render(link_text, True, (180, 220, 255))
    else:
        link_color = (100, 150, 255)
        link_render = fuente_chica.render(link_text, True, (100, 150, 255))

    ventana.blit(link_render, link_rect)

    pygame.display.flip()


def login_usuario():
    """
    Gestiona el login. Utiliza un mapeo Nombre->ID al inicio 
    y luego usa seek() para ir directamente al registro.
    """
    
    nombre = ""
    password = ""
    ingresando_password = False
    error = ""
    usuario_logueado = None
    login_activo = True
    
    current_width = WIDTH
    current_height = HEIGHT
    
    calcular_geometria(current_width, current_height)

    nombre_a_id = {}
    try:
        
        ##matriz
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                
                    partes = line.split(',')
                    if len(partes) >= 3:
                        user_id = partes[0].strip()
                        user_nombre = partes[1].strip()
                        nombre_a_id[user_nombre] = int(user_id)
    except FileNotFoundError:
        nombre_a_id = {}
    except Exception as e:
        print(f"Error al cargar mapeo de usuarios: {e}")
        nombre_a_id = {}


    while login_activo:
        cursor = pygame.SYSTEM_CURSOR_ARROW
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if link_rect.collidepoint(mouse_x, mouse_y):
            cursor = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor)
        
        pygame.mouse.set_cursor(cursor)       
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                calcular_geometria(current_width, current_height)

            # --- MANEJO DE CLICKS Y TECLA ENTER ---
            trigger_login = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect_boton.collidepoint(event.pos):
                trigger_login = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and ingresando_password:
                trigger_login = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if link_rect.collidepoint(mouse_x, mouse_y):
                    import webbrowser
                    webbrowser.open("https://github.com/Agustincito1")

                if rect_usuario.collidepoint(event.pos):
                    ingresando_password = False
                    error = ""
                elif rect_contrasena.collidepoint(event.pos):
                    ingresando_password = True
                    error = ""
            
            if trigger_login:
                nombre_limpio = nombre.strip()
                password_limpia = password.strip()

                if not nombre_limpio or not password_limpia:
                    error = "Por favor, introduce usuario y contraseña"
                else:
                    # 2. Verificar existencia y obtener ID
                    if nombre_limpio in nombre_a_id:
                        target_id = nombre_a_id[nombre_limpio]
                        
                        try:
                        
                            with open(RUTA_USUARIOS, "rb") as f:
                                
                                # Posición en bytes: (ID objetivo - 1) * Tamaño fijo del registro
                                offset = (target_id - 1) * REGISTRO_SIZE 
                                f.seek(offset)
                                
                                # Leemos exactamente el tamaño del registro (41 bytes)
                                registro_bytes = f.read(REGISTRO_SIZE)
                                print(registro_bytes)
                                # Verificación de lectura: si el archivo termina antes, no se pudo leer el registro completo
                                if len(registro_bytes) < REGISTRO_SIZE:
                                    error = "Registro incompleto o ID fuera de rango."
                                    nombre = ""; password = ""; ingresando_password = False
                                    continue # Ir al siguiente ciclo del while

                                # Decodificamos, pero solo limpiamos los espacios al final del registro (el \n) para el split
                                # Ahora usamos rstrip() para eliminar solo el \n, manteniendo el relleno interno
                                registro = registro_bytes.decode('utf-8').rstrip() 

                                # Desempaquetar el registro. Los campos nombre y pass aún tienen los espacios de relleno.
                                id_reg, nombre_reg_relleno, pass_reg_relleno = registro.split(',')
                                
                                # Limpiamos los espacios de relleno de la contraseña para la comparación
                                pass_almacenada = pass_reg_relleno.strip()
                                
                                if pass_almacenada == password_limpia:
                                    # ¡Login Exitoso!
                                    usuario_logueado = target_id
                                    login_activo = False
                                else:
                                    error = "Usuario o contraseña incorrectos"
                                    nombre = ""; password = ""; ingresando_password = False
                                    
                        except (IOError, ValueError, IndexError, UnicodeDecodeError):
                            # ... (Manejo de errores mantenido) ...
                            error = "Error al leer registro de usuario."
                            nombre = ""; password = ""; ingresando_password = False
                            
                    else:
                        error = "Usuario o contraseña incorrectos"
                        nombre = ""; password = ""; ingresando_password = False

            
            # --- MANEJO DE TECLADO (No Login) ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 
                
                elif event.key == pygame.K_BACKSPACE:
                    if not ingresando_password:
                        nombre = nombre[:-1]
                    else:
                        password = password[:-1]
                
                elif event.unicode.isprintable():
                    if not ingresando_password and len(nombre) < MAX_CARACTERES:
                        nombre += event.unicode
                    elif ingresando_password and len(password) < MAX_CARACTERES:
                        password += event.unicode

        dibujar_login(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y)
        clock.tick(FPS)

    return usuario_logueado


# --- El resto de funciones (Registro) se mantiene, solo se añade la ruta y se modifican las claves ---

def calcular_geometria_registro(current_width, current_height):
    """Calcula y actualiza todos los rectángulos para la pantalla de registro."""
    global rect_form_r, rect_nombre_r, rect_contrasena_r, rect_boton_r, RECT_ERROR_R
    global TITULO_Y_R, RECT_NOMBRE_Y_R, RECT_CONTRASENA_Y_R, RECT_BOTON_Y_R

    card_width = min(CARD_WIDTH_REL, current_width // 2)
    card_height = min(CARD_HEIGHT_REL, current_height - 100)

    CARD_X = int(current_width * 0.7) - (card_width // 2)
    CARD_Y = current_height // 2 - (card_height // 2)

    rect_form_r = pygame.Rect(CARD_X, CARD_Y, card_width, card_height)

    FIELD_WIDTH = int(card_width * 0.8)
    FIELD_HEIGHT = 40
    FIELD_X = CARD_X + (card_width - FIELD_WIDTH) // 2

    TITULO_Y_R = CARD_Y + 30 
    
    ETIQUETA_NOMBRE_Y_R = TITULO_Y_R + 70
    RECT_NOMBRE_Y_R = ETIQUETA_NOMBRE_Y_R + 25

    ETIQUETA_CONTRASENA_Y_R = RECT_NOMBRE_Y_R + FIELD_HEIGHT + 20
    RECT_CONTRASENA_Y_R = ETIQUETA_CONTRASENA_Y_R + 25

    RECT_BOTON_Y_R = RECT_CONTRASENA_Y_R + FIELD_HEIGHT + 40
    
    ERROR_Y_R = RECT_BOTON_Y_R + BOTON_HEIGHT + 15

    rect_nombre_r = pygame.Rect(FIELD_X, RECT_NOMBRE_Y_R, FIELD_WIDTH, FIELD_HEIGHT)
    rect_contrasena_r = pygame.Rect(FIELD_X, RECT_CONTRASENA_Y_R, FIELD_WIDTH, FIELD_HEIGHT)
    rect_boton_r = pygame.Rect(FIELD_X, RECT_BOTON_Y_R, FIELD_WIDTH, BOTON_HEIGHT)
    RECT_ERROR_R = pygame.Rect(FIELD_X, ERROR_Y_R, FIELD_WIDTH, 30)

# El resto de dibujar_registro es correcto y se mantiene
def dibujar_registro(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y):
    if rect_form_r is None:
        return
        
    ventana.blit(fondoMenuResponsive, (0, 0))

    # --- 1. DIBUJAR LOGO (Izquierda) ---
    if logoMenuResponsive:
        radio = min(current_width, current_height) // 5 
        size = radio * 2
        
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        logo_x = (current_width // 4) - (size // 2)
        logo_y = (current_height - size) // 2
        ventana.blit(circular_surface, (logo_x, logo_y))

    # --- 2. DIBUJAR PANEL DE REGISTRO (Derecha) ---

    # Panel de Registro (Tarjeta)
    pygame.draw.rect(ventana, COLOR_CARD_BACKGROUND, rect_form_r, border_radius=10)

    # Título "Registro"
    texto_titulo = fuente.render("Registro", True, COLOR_TITULO_Y_ETIQUETA)
    titulo_x = rect_form_r.x + (rect_form_r.width - texto_titulo.get_width()) // 2
    ventana.blit(texto_titulo, (titulo_x, TITULO_Y_R))

    # Etiquetas de Campos
    etiqueta_nombre = fuente_chica.render("Nombre de Usuario", True, COLOR_TITULO_Y_ETIQUETA)
    ventana.blit(etiqueta_nombre, (rect_nombre_r.x, rect_nombre_r.y - 25)) 
    etiqueta_contrasena = fuente_chica.render("Contraseña", True, COLOR_TITULO_Y_ETIQUETA)
    ventana.blit(etiqueta_contrasena, (rect_contrasena_r.x, rect_contrasena_r.y - 25))

    # Campos de Texto (Renderizados)
    texto_nombre = fuente_chica.render(nombre, True, BLANCO)
    pygame.draw.rect(ventana, COLOR_CAMPO_FONDO, rect_nombre_r, border_radius=5)
    text_y_nombre = rect_nombre_r.y + (rect_nombre_r.height - texto_nombre.get_height()) // 2
    ventana.blit(texto_nombre, (rect_nombre_r.x + 10, text_y_nombre))

    texto_password = "*"*len(password)
    texto_password_render = fuente_chica.render(texto_password, True, BLANCO)
    pygame.draw.rect(ventana, COLOR_CAMPO_FONDO, rect_contrasena_r, border_radius=5)
    text_y_contrasena = rect_contrasena_r.y + (rect_contrasena_r.height - texto_password_render.get_height()) // 2
    ventana.blit(texto_password_render, (rect_contrasena_r.x + 10, text_y_contrasena))

    # Botón
    pygame.draw.rect(ventana, COLOR_BOTON, rect_boton_r, border_radius=5)
    texto_boton = fuente_chica.render("Registrar", True, BLANCO)
    boton_text_x = rect_boton_r.x + (rect_boton_r.width - texto_boton.get_width()) // 2
    boton_text_y = rect_boton_r.y + (rect_boton_r.height - texto_boton.get_height()) // 2
    ventana.blit(texto_boton, (boton_text_x, boton_text_y))

    # Error
    if error:
        pygame.draw.rect(ventana, COLOR_FONDO_ERROR, RECT_ERROR_R, border_radius=5)
        error_render = fuente_chica2.render(error, True, COLOR_TEXTO_ERROR)
        error_x = RECT_ERROR_R.x + (RECT_ERROR_R.width - error_render.get_width()) // 2
        error_y = RECT_ERROR_R.y + (RECT_ERROR_R.height - error_render.get_height()) // 2
        ventana.blit(error_render, (error_x, error_y))
    
    if link_rect.collidepoint(mouse_x, mouse_y):
        link_color = (180, 220, 255)
        link_render = fuente_chica.render(link_text, True, (180, 220, 255))
    else:
        link_color = (100, 150, 255)
        link_render = fuente_chica.render(link_text, True, (100, 150, 255))

    ventana.blit(link_render, link_rect)
    pygame.display.flip()

# El resto de dibujar_registro_exitoso es correcto y se mantiene
def dibujar_registro_exitoso(ventana, width, height):
    """Dibuja el mensaje de éxito centrado en la pantalla."""
    
    TEXTO_EXITO = "¡Registro Exitoso!"
    TEXTO_MENU = "Regresando al menú principal..."
    
    COLOR_FONDO = (0, 150, 0) # Verde oscuro
    COLOR_TEXTO = (255, 255, 255) # Blanco
    
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))
    ventana.blit(s, (0, 0))

    render_exito = fuente.render(TEXTO_EXITO, True, COLOR_TEXTO)
    render_menu = fuente_chica.render(TEXTO_MENU, True, COLOR_TEXTO)
    
    exito_x = (width - render_exito.get_width()) // 2
    exito_y = height // 2 - render_exito.get_height() - 10
    
    menu_x = (width - render_menu.get_width()) // 2
    menu_y = height // 2 + 10

    PANEL_WIDTH = max(render_exito.get_width(), render_menu.get_width()) + 80
    PANEL_HEIGHT = render_exito.get_height() + render_menu.get_height() + 80
    
    panel_rect = pygame.Rect((width - PANEL_WIDTH) // 2, (height - PANEL_HEIGHT) // 2, PANEL_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(ventana, COLOR_FONDO, panel_rect, border_radius=15)
    
    ventana.blit(render_exito, (exito_x, exito_y))
    ventana.blit(render_menu, (menu_x, menu_y))
    
    pygame.display.flip()


def registro_usuario():
    cursor = pygame.SYSTEM_CURSOR_ARROW 
    pygame.mouse.set_cursor(cursor)
    
    nombre = ""
    password = ""
    registrando = True
    ingresando_password = False
    registro_exitoso = False
    error = ""
    
    current_width = WIDTH
    current_height = HEIGHT
    calcular_geometria_registro(current_width, current_height)

    # Asegurarse de que la carpeta existe
    os.makedirs(os.path.dirname(RUTA_USUARIOS), exist_ok=True)

    # Leer usuarios existentes
    lineas = []
    usuarios = []
    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped:
                    lineas.append(line_stripped)
                    # El nombre es el segundo campo (índice 1), lo obtenemos limpio
                    try:
                        nombre_limpio = line_stripped.split(",")[1].strip()
                        usuarios.append(nombre_limpio)
                    except IndexError:
                        # Registro corrupto, se ignora el nombre para la verificación
                        pass
    except FileNotFoundError:
        pass

    # Calcular próximo ID
    if lineas:
        # El ID es el primer campo (índice 0)
        try:
            ultimo_id = int(lineas[-1].split(",")[0].strip())
        except ValueError:
             ultimo_id = 0
    else:
        ultimo_id = 0

    while registrando:
        cursor = pygame.SYSTEM_CURSOR_ARROW
        mouse_x, mouse_y = pygame.mouse.get_pos()

        try:
            if link_rect.collidepoint(mouse_x, mouse_y):
                cursor = pygame.SYSTEM_CURSOR_HAND
            pygame.mouse.set_cursor(cursor)
        except NameError:
            pass
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                current_width, current_height = event.size
                calcular_geometria_registro(current_width, current_height)

            # --- MANEJO DE CLICKS DEL RATÓN ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    try:
                        if link_rect.collidepoint(mouse_x, mouse_y):
                            import webbrowser
                            webbrowser.open("https://github.com/Agustincito1")
                    except NameError:
                          pass

                    if rect_nombre_r.collidepoint(event.pos):
                        ingresando_password = False
                        error = ""
                    elif rect_contrasena_r.collidepoint(event.pos):
                        ingresando_password = True
                        error = ""
                    elif rect_boton_r.collidepoint(event.pos):
                        # Validación al hacer clic en el botón
                        (ingresando_password, error, registrando, nombre, 
                         password, usuarios, ultimo_id, status) = validar_registro(
                            nombre, password, usuarios, ultimo_id, error, registrando, 
                            ingresando_password, True
                        )
                        if not registrando and status:
                            registro_exitoso = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validación al presionar ENTER
                    (ingresando_password, error, registrando, nombre, 
                     password, usuarios, ultimo_id, status) = validar_registro(
                        nombre, password, usuarios, ultimo_id, error, registrando, 
                        ingresando_password, False
                    )
                    if not registrando and status:
                        registro_exitoso = True

                elif event.key == pygame.K_BACKSPACE:
                    if not ingresando_password:
                        nombre = nombre[:-1]
                    else:
                        password = password[:-1]

                elif event.key == pygame.K_ESCAPE:
                    registrando = False
                    error = ""

                else:
                    # Implementación del límite de caracteres
                    if event.unicode.isprintable():
                        if not ingresando_password and len(nombre) < MAX_CARACTERES:
                            nombre += event.unicode
                        elif ingresando_password and len(password) < MAX_CARACTERES:
                            password += event.unicode
        
        dibujar_registro(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y)
        clock.tick(FPS)
    
    if registro_exitoso:
        tiempo_inicio = time.time()
        while time.time() - tiempo_inicio < 1.5:
            dibujar_registro_exitoso(ventana, current_width, current_height)
            clock.tick(FPS)
            
        return True

    return False


def validar_registro(nombre, password, usuarios, ultimo_id, current_error, current_registrando, current_ingresando_password, is_button_click):
    """
    Función auxiliar para manejar la validación y avance del registro.
    Asegura la longitud fija de los campos al escribir.
    """
    nombre_limpio = nombre.strip()
    password_limpia = password.strip()
    
    error_temp = ""
    registrando_temp = current_registrando
    ingresando_password_temp = current_ingresando_password
    
    usuarios_actualizados = usuarios
    ultimo_id_actualizado = ultimo_id
    return_status = False

    if not current_ingresando_password:
        # Etapa: Introducir Nombre
        if not nombre_limpio:
            error_temp = "El nombre de usuario no puede estar vacío."
        elif nombre_limpio in usuarios:
            error_temp = "¡Ese usuario ya existe! Elige otro."
            nombre = ""
        elif is_button_click or not is_button_click:
              # Avanzar al campo de contraseña
             ingresando_password_temp = True
             password = ""

    elif current_ingresando_password:
        # Etapa: Introducir Contraseña o Intentar Guardar
        if not password_limpia:
            error_temp = "La contraseña no puede estar vacía."
             
        elif nombre_limpio in usuarios:
             # Falla de seguridad (no debería ocurrir si la lógica es secuencial)
             error_temp = "¡Error! Este nombre de usuario ya existe."
             registrando_temp = True
             ingresando_password_temp = False
             nombre = ""
             password = ""
             
        else:
            # Registro exitoso
            if not error_temp:
                nuevo_id = ultimo_id + 1
                
                # --- FORMATO DE LONGITUD FIJA CON LJUST() ---
                # Rellenamos con espacios hasta el tamaño máximo
                id_formateado = str(nuevo_id).zfill(LONGITUD_ID) # Usamos zfill para rellenar ID con ceros
                nombre_formateado = nombre_limpio.ljust(MAX_CARACTERES)
                password_formateada = password_limpia.ljust(MAX_CARACTERES)
                # ---------------------------------------------
                
                try:
                    # Abrimos en modo texto para escribir la línea de texto
                    with open(RUTA_USUARIOS, "a", encoding="utf-8") as f:
                        # Escribimos el registro de 41 bytes (2+1+18+1+18+1 = 41)
                        f.write(f"{id_formateado},{nombre_formateado},{password_formateada}\n")
                    
                    usuarios_actualizados = usuarios + [nombre_limpio]
                    ultimo_id_actualizado = nuevo_id
                    
                    registrando_temp = False
                    return_status = True # ÉXITO CONFIRMADO
                except Exception:
                    error_temp = "Error al guardar el usuario."
                
    return (ingresando_password_temp, error_temp, registrando_temp, nombre, 
            password, usuarios_actualizados, ultimo_id_actualizado, return_status)







import logging
import os
from datetime import datetime

try:
    from config import (
        REGISTRO_SIZE, LONGITUD_PUNTERO_PRINCIPAL, RUTA_USUARIOS
    )
except ImportError:
    REGISTRO_SIZE = 41
    LONGITUD_PUNTERO_PRINCIPAL = 5
    RUTA_USUARIOS = "./utils/regist/usuarios.txt"
    OFFSET_A_PUNTERO_PRINCIPAL = 41

REGISTRO_EVENTO_SIZE = 36
LONGITUD_PUNTERO_EVENTO = 5
LONGITUD_EVENTO = 12
LONGITUD_ID_USUARIO = 4
RUTA_REGISTRO_EVENTOS = "./utils/regist/resultados.txt"
OFFSET_A_REGSIG = 24


def obtener_ultimo_registro_y_tamano():
    try:
        os.makedirs(os.path.dirname(RUTA_REGISTRO_EVENTOS), exist_ok=True)
        if not os.path.exists(RUTA_REGISTRO_EVENTOS):
            return 0, 0
        with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
            f.seek(0, 2)
            tamano_archivo = f.tell()
            ultimo_registro_numero = tamano_archivo // REGISTRO_EVENTO_SIZE 
            return tamano_archivo, ultimo_registro_numero
    except Exception as e:
        print(f"Error al obtener tamaño del registro: {e}")
        return 0, 0

def actualizar_puntero_siguiente(registro_a_actualizar, puntero_siguiente):
    offset_registro = (registro_a_actualizar - 1) * REGISTRO_EVENTO_SIZE
    offset_a_escribir = offset_registro + OFFSET_A_REGSIG
    nuevo_puntero_formateado = str(puntero_siguiente).zfill(LONGITUD_PUNTERO_EVENTO)
    try:
        with open(RUTA_REGISTRO_EVENTOS, "r+b") as f:
            f.seek(offset_a_escribir)
            f.write(nuevo_puntero_formateado.encode('utf-8'))
    except Exception as e:
        print(f"Error al actualizar puntero 'Siguiente' del registro {registro_a_actualizar}: {e}")

def registrar_resultado(id_usuario, resultado):
    if id_usuario is None:
        return []

    fecha = datetime.now().strftime("%Y-%m-%d")
    resultado_norm = (resultado[0].upper() if resultado else "N")    


    tamano_total, num_registros_actuales = obtener_ultimo_registro_y_tamano()
    nuevo_registro_numero = num_registros_actuales + 1
    ultimo_registro_anterior = num_registros_actuales
    ultimo_registro_mismo_usuario = 0
    

    if num_registros_actuales > 0:
        with open(RUTA_REGISTRO_EVENTOS, "rb") as f:
            for i in range(num_registros_actuales, 0, -1):
                offset = (i - 1) * REGISTRO_EVENTO_SIZE
                f.seek(offset + 6) 
                id_reg = f.read(4).decode('utf-8')
                if id_reg == str(id_usuario).zfill(LONGITUD_ID_USUARIO):
                    ultimo_registro_mismo_usuario = i
                    break

    if ultimo_registro_mismo_usuario > 0:
        reg_ant_puntero = str(ultimo_registro_mismo_usuario).zfill(LONGITUD_PUNTERO_EVENTO)    
    else:
        reg_ant_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
        
    
    reg_sig_puntero = "0".zfill(LONGITUD_PUNTERO_EVENTO)
    num_registro_formateado = str(nuevo_registro_numero).zfill(LONGITUD_PUNTERO_EVENTO)
    id_formateado = str(id_usuario).zfill(LONGITUD_ID_USUARIO)

    nuevo_registro_str = (
        f"{num_registro_formateado},"
        f"{id_formateado},"
        f"{fecha},"
        f"{resultado_norm},"
        f"{reg_sig_puntero},"
        f"{reg_ant_puntero}"
        f"\n"
    )
    
    nuevo_registro_bytes = nuevo_registro_str.encode('utf-8')
        
    if len(nuevo_registro_bytes) != REGISTRO_EVENTO_SIZE:
        print(f"ERROR CRÍTICO DE TAMAÑO: {len(nuevo_registro_bytes)} != {REGISTRO_EVENTO_SIZE}")
        return


    try:
        with open(RUTA_REGISTRO_EVENTOS, "ab") as f:
            f.write(nuevo_registro_bytes)
        if ultimo_registro_mismo_usuario > 0:
            actualizar_puntero_siguiente(ultimo_registro_mismo_usuario, nuevo_registro_numero)

    except Exception as e:
        print(f"Error al registrar evento: {e}")

    return 
