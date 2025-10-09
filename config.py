import pygame
pygame.init()
pygame.display.set_caption("Ronaldinho")
WIDTH, HEIGHT = 1200, 800
NEGRO = (0, 0, 0)
# Color de selección/énfasis — cambiado a naranja para mejor contraste con el fondo #041F37
ROJO = (255, 165, 0)
BLANCO = (255, 255, 255)
menu_opciones = ["Jugar", "Registrarse", "Ranking", "Salir"]
opcion = 0
goles_jugador = 0
goles_bot = 0
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
fondo = pygame.image.load("./utils/imgs/estadio.jpg")
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
duracion_partido = 10
tiempo_inicio = pygame.time.get_ticks()
partido_terminado = False


link_text = "@Agustincito1"
color_link = (100, 150, 255)  # celeste
link_render = fuente_chica.render(link_text, True, color_link)
link_rect = link_render.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))


