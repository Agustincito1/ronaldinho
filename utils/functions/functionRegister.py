import pygame
import time 
import sys
# Asegúrate de que config.py contenga todas estas variables.
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, FPS, clock, fuente, fondoMenuResponsive, fuente_chica, fuente_chica2, AZUL_OSCURO, logoMenuResponsive, BLANCOG, link_rect, link_text

pygame.init()

# --- Estilos de Apariencia (Mantenidos) ---
COLOR_CARD_BACKGROUND = (230, 230, 230)
COLOR_CAMPO_FONDO = (38, 43, 59)
COLOR_TITULO_Y_ETIQUETA = (50, 50, 50)
COLOR_BOTON = (43, 110, 219)
CARD_WIDTH_REL = 400
CARD_HEIGHT_REL = 400
BOTON_HEIGHT = 50
MAX_CARACTERES = 18  # Límite de caracteres para los inputs
# Nuevo estilo para la alerta de error
COLOR_FONDO_ERROR = (255, 100, 100) # Un rojo más suave de fondo
COLOR_TEXTO_ERROR = (150, 0, 0)     # Rojo oscuro para la letra

# --- Variables Globales para Geometría (Mantenidas) ---
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


def calcular_geometria(current_width, current_height):
    """Calcula y actualiza todos los rectángulos de la interfaz en base a las dimensiones actuales."""
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
    # Nuevo rectángulo para el fondo del mensaje de error
    RECT_ERROR = pygame.Rect(FIELD_X, ERROR_Y, FIELD_WIDTH, 30)


def dibujar_login(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y):
    if rect_form is None:
        return
        
    ventana.blit(fondoMenuResponsive, (0, 0))

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

    
    nombre = ""
    password = ""
    ingresando_password = False
    error = ""
    usuario_logueado = None
    login_activo = True
    
    current_width = WIDTH
    current_height = HEIGHT
    
    calcular_geometria(current_width, current_height)

    try:
        with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
            usuarios = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        usuarios = []

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

            # --- MANEJO DE CLICKS DEL RATÓN ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if link_rect.collidepoint(mouse_x, mouse_y):
                        import webbrowser
                        webbrowser.open("https://github.com/Agustincito1")

                if rect_usuario.collidepoint(event.pos):
                    ingresando_password = False
                    error = ""
                elif rect_contrasena.collidepoint(event.pos):
                    ingresando_password = True
                    error = ""
                elif rect_boton.collidepoint(event.pos):
                    if nombre and password:
                        for u in usuarios:
                            uid, n, p = u
                            if n == nombre and p == password:
                                usuario_logueado = int(uid)
                                login_activo = False
                                break
                        else:
                            error = "Usuario o contraseña incorrectos"
                            nombre = ""
                            password = ""
                            ingresando_password = False
                    else:
                        error = "Por favor, introduce usuario y contraseña"

            if event.type == pygame.KEYDOWN:
                # 1. Manejo de la tecla ESC para salir
                if event.key == pygame.K_ESCAPE:
                    return 

                if event.key == pygame.K_RETURN:
                    if not ingresando_password:
                        ingresando_password = True
                    else:
                        if nombre and password:
                            for u in usuarios:
                                uid, n, p = u
                                if n == nombre and p == password:
                                    usuario_logueado = int(uid)
                                    login_activo = False
                                    break
                            else:
                                error = "Usuario o contraseña incorrectos"
                                nombre = ""
                                password = ""
                                ingresando_password = False
                        else:
                            error = "Por favor, introduce usuario y contraseña"

                elif event.key == pygame.K_BACKSPACE:
                    if not ingresando_password:
                        nombre = nombre[:-1]
                    else:
                        password = password[:-1]
                else:
                    # 2. Implementación del límite de caracteres
                    if event.unicode.isprintable():
                        if not ingresando_password and len(nombre) < MAX_CARACTERES:
                            nombre += event.unicode
                        elif ingresando_password and len(password) < MAX_CARACTERES:
                            password += event.unicode

        dibujar_login(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y)
        clock.tick(FPS)


        


    

    return usuario_logueado



def calcular_geometria_registro(current_width, current_height):
    """Calcula y actualiza todos los rectángulos para la pantalla de registro, posicionando el formulario a la derecha."""
    global rect_form_r, rect_nombre_r, rect_contrasena_r, rect_boton_r, RECT_ERROR_R
    global TITULO_Y_R, RECT_NOMBRE_Y_R, RECT_CONTRASENA_Y_R, RECT_BOTON_Y_R

    # Dimensiones de la Tarjeta (Formulario)
    card_width = min(CARD_WIDTH_REL, current_width // 2)
    card_height = min(CARD_HEIGHT_REL, current_height - 100)

    # Posicionamiento: El centro de la tarjeta está a ~70% del ancho (DERECHA), centrado verticalmente
    CARD_X = int(current_width * 0.7) - (card_width // 2)
    CARD_Y = current_height // 2 - (card_height // 2)

    rect_form_r = pygame.Rect(CARD_X, CARD_Y, card_width, card_height)

    FIELD_WIDTH = int(card_width * 0.8)
    FIELD_HEIGHT = 40
    FIELD_X = CARD_X + (card_width - FIELD_WIDTH) // 2

    TITULO_Y_R = CARD_Y + 30 
    
    # Campo Nombre de Usuario
    ETIQUETA_NOMBRE_Y_R = TITULO_Y_R + 70
    RECT_NOMBRE_Y_R = ETIQUETA_NOMBRE_Y_R + 25

    # Campo Contraseña
    ETIQUETA_CONTRASENA_Y_R = RECT_NOMBRE_Y_R + FIELD_HEIGHT + 20
    RECT_CONTRASENA_Y_R = ETIQUETA_CONTRASENA_Y_R + 25

    # Botón Registrar
    RECT_BOTON_Y_R = RECT_CONTRASENA_Y_R + FIELD_HEIGHT + 40
    
    # Posición del mensaje de error
    ERROR_Y_R = RECT_BOTON_Y_R + BOTON_HEIGHT + 15

    # Rectángulos finales
    rect_nombre_r = pygame.Rect(FIELD_X, RECT_NOMBRE_Y_R, FIELD_WIDTH, FIELD_HEIGHT)
    rect_contrasena_r = pygame.Rect(FIELD_X, RECT_CONTRASENA_Y_R, FIELD_WIDTH, FIELD_HEIGHT)
    rect_boton_r = pygame.Rect(FIELD_X, RECT_BOTON_Y_R, FIELD_WIDTH, BOTON_HEIGHT)
    RECT_ERROR_R = pygame.Rect(FIELD_X, ERROR_Y_R, FIELD_WIDTH, 30)


def dibujar_registro(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y):
    if rect_form_r is None:
        return
        
    ventana.blit(fondoMenuResponsive, (0, 0))

    # --- 1. DIBUJAR LOGO (Izquierda) ---
    if logoMenuResponsive:
        radio = min(current_width, current_height) // 5 # Usamos el mismo tamaño del login
        size = radio * 2
        
        Imagen = pygame.transform.smoothscale(logoMenuResponsive, (size, size))
        circular_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        mask = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (radio, radio), radio)
        circular_surface.blit(Imagen, (0, 0))
        circular_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Posición del logo: Centrado en el cuarto izquierdo
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

# (Asumo que todas las constantes, como WIDTH, HEIGHT, FPS, rect_nombre_r, etc., están definidas
# y que la función 'dibujar_registro' y 'calcular_geometria_registro' están disponibles en este ámbito)

def dibujar_registro_exitoso(ventana, width, height):
    """Dibuja el mensaje de éxito centrado en la pantalla."""
    
    TEXTO_EXITO = "¡Registro Exitoso!"
    TEXTO_MENU = "Regresando al menú principal..."
    
    COLOR_FONDO = (0, 150, 0) # Verde oscuro
    COLOR_TEXTO = (255, 255, 255) # Blanco
    
    # 1. Dibujar un fondo semitransparente para la alerta
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150)) # Fondo negro con 150 de transparencia
    ventana.blit(s, (0, 0))

    # 2. Renderizar textos
    render_exito = fuente.render(TEXTO_EXITO, True, COLOR_TEXTO)
    render_menu = fuente_chica.render(TEXTO_MENU, True, COLOR_TEXTO)
    
    # 3. Calcular posición (Centrado)
    exito_x = (width - render_exito.get_width()) // 2
    exito_y = height // 2 - render_exito.get_height() - 10
    
    menu_x = (width - render_menu.get_width()) // 2
    menu_y = height // 2 + 10

    # 4. Dibujar el panel de la alerta
    PANEL_WIDTH = max(render_exito.get_width(), render_menu.get_width()) + 80
    PANEL_HEIGHT = render_exito.get_height() + render_menu.get_height() + 80
    
    panel_rect = pygame.Rect((width - PANEL_WIDTH) // 2, (height - PANEL_HEIGHT) // 2, PANEL_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(ventana, COLOR_FONDO, panel_rect, border_radius=15)
    
    # 5. Dibujar textos en el panel
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
    registro_exitoso = False # Nuevo estado para la alerta
    error = ""
    
    current_width = WIDTH
    current_height = HEIGHT
    calcular_geometria_registro(current_width, current_height)



    # Leer usuarios existentes
    try:
        with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
            lineas = [line.strip() for line in f if line.strip()]
            usuarios = [line.split(",")[1] for line in lineas]
    except FileNotFoundError:
        lineas = []
        usuarios = []

    # Calcular próximo ID
    if lineas:
        ultimo_id = int(lineas[-1].split(",")[0])
    else:
        ultimo_id = 0

    while registrando:
        cursor = pygame.SYSTEM_CURSOR_ARROW
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Manejo de cursor
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

            # Manejo de Redimensionamiento
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
                    ingresando_password, error, registrando, nombre, password, usuarios, ultimo_id, status = validar_registro(
                        nombre, password, usuarios, ultimo_id, error, registrando, ingresando_password, True
                    )
                    # VERIFICACIÓN DE ESTADO DE ÉXITO
                    if not registrando and status:
                        registro_exitoso = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ingresando_password, error, registrando, nombre, password, usuarios, ultimo_id, status = validar_registro(
                        nombre, password, usuarios, ultimo_id, error, registrando, ingresando_password, False
                    )
                    # VERIFICACIÓN DE ESTADO DE ÉXITO
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
        
        # Dibujado normal
        dibujar_registro(nombre, password, error, ingresando_password, current_width, current_height, mouse_x, mouse_y)
        clock.tick(FPS)
    
    # --- MANEJO DE ALERTA Y SALIDA AL MENÚ PRINCIPAL ---
    if registro_exitoso:
        tiempo_inicio = time.time()
        # Bucle de la alerta
        while time.time() - tiempo_inicio < 1.5: # Muestra la alerta por 1.5 segundos
            # No necesitamos procesar eventos aquí, solo dibujar
            dibujar_registro_exitoso(ventana, current_width, current_height)
            clock.tick(FPS)
            
        return True # Registro exitoso, ir al menú

    return False # Salida por ESCAPE


def validar_registro(nombre, password, usuarios, ultimo_id, current_error, current_registrando, current_ingresando_password, is_button_click):
    """
    Función auxiliar para manejar la validación y avance del registro.
    Retorna (ingresando_password, error, registrando, nombre, password, usuarios_actualizados, ultimo_id_actualizado, return_status)
    """
    nombre_limpio = nombre.strip()
    password_limpia = password.strip()
    
    error_temp = ""
    registrando_temp = current_registrando
    ingresando_password_temp = current_ingresando_password
    
    usuarios_actualizados = usuarios
    ultimo_id_actualizado = ultimo_id
    return_status = False # NUEVO: Por defecto, no es un registro exitoso

    if not current_ingresando_password:
        # Etapa: Introducir Nombre
        if not nombre_limpio:
            error_temp = "El nombre de usuario no puede estar vacío."
        elif nombre_limpio in usuarios:
            error_temp = "¡Ese usuario ya existe! Elige otro."
            nombre = ""
        elif is_button_click or not is_button_click:
             ingresando_password_temp = True
             password = ""

    elif current_ingresando_password:
        # Etapa: Introducir Contraseña o Intentar Guardar
        if not password_limpia:
            error_temp = "La contraseña no puede estar vacía."
             
        elif nombre_limpio in usuarios:
             # Falla en la verificación de seguridad
             error_temp = "¡Error crítico! Este nombre de usuario ya existe."
             registrando_temp = True
             ingresando_password_temp = False
             nombre = ""
             password = ""
             
        else:
            # Registro exitoso
            if not error_temp:
                nuevo_id = ultimo_id + 1
                try:
                    with open("./utils/regist/usuarios.txt", "a", encoding="utf-8") as f:
                        f.write(f"{nuevo_id},{nombre_limpio},{password_limpia}\n")
                    
                    usuarios_actualizados = usuarios + [nombre_limpio]
                    ultimo_id_actualizado = nuevo_id
                    
                    registrando_temp = False
                    return_status = True # ÉXITO CONFIRMADO
                except Exception:
                    error_temp = "Error al guardar el usuario."
                
    # El retorno incluye los 8 valores
    return ingresando_password_temp, error_temp, registrando_temp, nombre, password, usuarios_actualizados, ultimo_id_actualizado, return_status


from datetime import datetime

def registrar_resultado(user_id, resultado, archivo="./utils/regist/resultados.txt"):
    fecha = datetime.now().strftime("%Y-%m-%d")  # Solo fecha
    try:
        with open(archivo, "a", encoding="utf-8") as f:
            f.write(f"{user_id},{resultado},{fecha}\n")
    except Exception as e:
        print("❌ Error al registrar resultado:", e)
