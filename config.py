import pygame
pygame.init()
pygame.display.set_caption("Ronaldinho")
WIDTH, HEIGHT = 1200, 600
NEGRO = (0, 0, 0)
ROJO = (0, 0, 255)
BLANCO = (255, 255, 255)
menu_opciones = ["Jugar", "Registrarse", "Ranking", "Salir"]
opcion = 0
goles_jugador = 0
goles_bot = 0
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
fondo = pygame.image.load("./utils/imgs/estadio.jpg")
fondoMenu = pygame.image.load("./utils/imgs/ronaldinho.png")
fondoResponsive = pygame.transform.scale(fondo, (WIDTH, HEIGHT))
fondoMenuResponsive = pygame.transform.scale(fondoMenu, (WIDTH, HEIGHT))
fuente = pygame.font.Font(None, 120)
fuente.set_bold(True)  
fuente_chica = pygame.font.Font(None, 36)
duracion_partido = 10
tiempo_inicio = pygame.time.get_ticks()
partido_terminado = False