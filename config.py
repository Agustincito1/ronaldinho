import pygame
pygame.init()
pygame.display.set_caption("Ronaldinho")
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
PANTALLA = pygame.display.set_mode(
    (WIDTH, HEIGHT), 
    pygame.FULLSCREEN
)
NEGRO = (0, 0, 0)
# Color de selección/énfasis — cambiado a naranja para mejor contraste con el fondo #041F37
ROJO = (255, 165, 0)
BLANCO = (255, 255, 255)
BLANCOG = (217, 217, 217)
AZUL_OSCURO = (10, 25, 50)
menu_opciones = ["Inicia Sesion", "Registrarse", "Salir"]
menu_juego = ["Jugar", "Ranking", "Preguntas (Puntos)", "Skins", "Salir"]
opcion = 0
goles_jugador = 0
goles_bot = 0
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
fondo = pygame.image.load("./utils/imgs/es.jpeg")
fondoResponsive = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
MENU_BG_COLOR = (4, 31, 55)
fondoMenuResponsive = pygame.Surface((WIDTH, HEIGHT))
fondoMenuResponsive.fill(MENU_BG_COLOR)
# Logo ronaldino
try:
	_logo = pygame.image.load("./utils/imgs/iconoR.png")
	# Escalar logo a un tamaño razonable según ancho
	logo_width = min(300, WIDTH // 3)
	logo_height = int(_logo.get_height() * (logo_width / _logo.get_width()))
	logoMenuResponsive = pygame.transform.scale(_logo, (logo_width, logo_height))
except Exception:
	logoMenuResponsive = None

fuente = pygame.font.Font(None, 120)
fuente.set_bold(True)  
fuente_chica = pygame.font.Font(None, 36)
duracion_partido = 1
tiempo_inicio = pygame.time.get_ticks()
partido_terminado = False


link_text = "@Agustincito1"
color_link = (100, 150, 255)  # celeste
link_render = fuente_chica.render(link_text, True, color_link)
link_rect = link_render.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))

GROUND_OFFSET = 40
RUTA_FUENTE_PRINCIPAL = "./utils/assets/font/InstrumentSans-VariableFont_wdth,wght.ttf" 
TAMAÑO_FUENTE_GRANDE = 75
TAMAÑO_FUENTE_CHICA = 35
TAMAÑO_FUENTE_CHICA2 = 20
# Carga la nueva fuente
try:
    # Esta es la variable que se importa como 'fuente'
    fuente = pygame.font.Font(RUTA_FUENTE_PRINCIPAL, TAMAÑO_FUENTE_GRANDE) 
    # Esta es la variable que se importa como 'fuente_chica'
    fuente_chica = pygame.font.Font(RUTA_FUENTE_PRINCIPAL, TAMAÑO_FUENTE_CHICA) 
    fuente_chica2 = pygame.font.Font(RUTA_FUENTE_PRINCIPAL, TAMAÑO_FUENTE_CHICA2) 
except FileNotFoundError:
    # Si el archivo no se encuentra, usa la fuente predeterminada del sistema
    print(f"Advertencia: Archivo de fuente no encontrado en {RUTA_FUENTE_PRINCIPAL}. Usando la fuente por defecto.")
    fuente = pygame.font.Font(None, TAMAÑO_FUENTE_GRANDE)
    fuente_chica = pygame.font.Font(None, TAMAÑO_FUENTE_CHICA)
    fuente_chica2 = pygame.font.Font(None, TAMAÑO_FUENTE_CHICA2)


try:
	arcoImg = pygame.image.load("./utils/imgs/arcos.png")
except Exception:
	logoMenuResponsive = None
	

    # ID (2 caracteres) + , (1) + Nombre (18) + , (1) + Contraseña (18) + \n (1) = 41 bytes
REGISTRO_SIZE = 41
MAX_CARACTERES = 18 
# Asumiendo que el ID nunca superará 99. Si lo hace, debes aumentar REGISTRO_SIZE.
LONGITUD_ID = 2