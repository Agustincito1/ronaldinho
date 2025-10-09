import pygame
import sys
from funciones import resumenCol


def SacarUsuario(id):
    # Leer usuarios
    usuario = ""
    with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if int(partes[0]) == int(id):
                if len(partes) >= 2:
                    usuario = partes[1]
    return usuario

# Inicializar pygame
pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("📊 Registro de Colisiones")

# Fuentes y colores
font = pygame.font.SysFont("consolas", 28, bold=True)
big_font = pygame.font.SysFont("consolas", 40, bold=True)

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)
BG_COLOR = (25, 25, 25)
BOX_COLOR = (45, 45, 45)
HIGHLIGHT_COLOR = (70, 70, 70)

# Opciones del menú
options = ["📂 Ver registro de los usuarios",
           "🔎 Año y mes usuario específico"]
selected = 0


# ------------------- DIBUJAR MENÚ -------------------
def draw_menu():
    screen.fill(BG_COLOR)
    title = big_font.render("MENÚ PRINCIPAL", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    for i, option in enumerate(options):
        color = YELLOW if i == selected else GRAY
        bg_rect = pygame.Rect(100, 150 + i * 80, WIDTH - 200, 60)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR if i == selected else BOX_COLOR, bg_rect, border_radius=10)
        text = font.render(option, True, color)
        screen.blit(text, (bg_rect.x + 20, bg_rect.y + 15))

    pygame.display.flip()


# ------------------- MOSTRAR RESUMEN -------------------
def mostrar_resumen():
    resumenCol()
    with open("./utils/regist/resumen.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    running = True
    col_widths = [80, 220, 100, 100, 100, 100]  # Ancho de cada columna
    x_start = 50
    row_height = 38
    header_bg = (35, 35, 60)
    even_row_bg = (40, 40, 40)
    odd_row_bg = (55, 55, 55)
    border_color = (90, 90, 90)

    while running:
        screen.fill(BG_COLOR)
        header = big_font.render("📊 Resumen de Todos los Usuarios", True, GREEN)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        y = 100
        # Dibujar fondo del encabezado
        pygame.draw.rect(screen, header_bg, (x_start, y, sum(col_widths), row_height), border_radius=8)
        # Dibujar encabezados de columna
        encabezados = ["ID", "Nombre", "Pelota", "ArcoD", "ArcoI", "Bot"]
        x = x_start
        for i, enc in enumerate(encabezados):
            text = font.render(enc, True, YELLOW)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[i]
        y += row_height

        # Dibujar filas de datos
        for idx, linea in enumerate(lineas):
            partes = linea.strip().split(",")
            if len(partes) == 6:
                row_bg = even_row_bg if idx % 2 == 0 else odd_row_bg
                pygame.draw.rect(screen, row_bg, (x_start, y, sum(col_widths), row_height))
                # Dibujar borde inferior
                pygame.draw.line(screen, border_color, (x_start, y + row_height), (x_start + sum(col_widths), y + row_height), 2)
                x = x_start
                for i, valor in enumerate(partes):
                    color = WHITE if i != 1 else GREEN
                    text = font.render(valor, True, color)
                    screen.blit(text, (x + 10, y + 5))
                    x += col_widths[i]
                y += row_height

        # Dibujar borde exterior de la tabla
        pygame.draw.rect(screen, border_color, (x_start, 100, sum(col_widths), y - 100), 3, border_radius=10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# ------------------- INPUT DE TEXTO -------------------
def pedir_texto_pygame(mensaje):
    texto = ""
    activo = True
    while activo:
        screen.fill(BG_COLOR)
        prompt = font.render(mensaje, True, YELLOW)
        screen.blit(prompt, (50, 200))

        caja = pygame.Rect(50, 260, 500, 50)
        pygame.draw.rect(screen, BOX_COLOR, caja, border_radius=8)
        input_text = font.render(texto, True, WHITE)
        screen.blit(input_text, (caja.x + 10, caja.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    texto = texto[:-1]
                elif event.unicode.isprintable():
                    texto += event.unicode
    return texto


# ------------------- REGISTRO POR AÑO -------------------
def mostrar_registro_por_anio_mes():
    usuario_id = pedir_texto_pygame("Ingrese el ID del usuario: ")
    anio = pedir_texto_pygame("Ingrese el año (ej: 2025): ")

    # Obtener el nombre del usuario usando la función sacar_usuario
    try:
        usuario_nombre = SacarUsuario(usuario_id)
        if not usuario_nombre:
            usuario_nombre = usuario_id
    except Exception:
        usuario_nombre = usuario_id

    meses = {str(m).zfill(2): {"Pelota": 0, "ArcoDerecho": 0, "ArcoIzquierdo": 0, "Bot": 0} for m in range(1, 13)}
    nombres_meses = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio",
        "07": "Julio", "08": "Agosto", "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }

    with open("./utils/regist/registro.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) < 3:
                continue
            id_usuario, fecha, tipo = partes[:3]
            if id_usuario == usuario_id and fecha.startswith(anio):
                mes = fecha.split("-")[1]
                if tipo in meses[mes]:
                    meses[mes][tipo] += 1

    running = True
    col_widths = [200, 120, 120, 120, 120]  # Mes, Pelota, ArcoD, ArcoI, Bot
    x_start = 50
    row_height = 38
    header_bg = (35, 35, 60)
    even_row_bg = (40, 40, 40)
    odd_row_bg = (55, 55, 55)
    border_color = (90, 90, 90)

    while running:
        screen.fill(BG_COLOR)
        header = big_font.render(f"📅 Colisiones de {usuario_nombre} en {anio}", True, GREEN)
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, 20))

        y = 100
        # Dibujar fondo del encabezado
        pygame.draw.rect(screen, header_bg, (x_start, y, sum(col_widths), row_height), border_radius=8)
        encabezados = ["Mes", "Pelota", "ArcoD", "ArcoI", "Bot"]
        x = x_start
        for i, enc in enumerate(encabezados):
            text = font.render(enc, True, YELLOW)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[i]
        y += row_height

        # Dibujar filas de datos
        for idx, (mes, datos) in enumerate(meses.items()):
            row_bg = even_row_bg if idx % 2 == 0 else odd_row_bg
            pygame.draw.rect(screen, row_bg, (x_start, y, sum(col_widths), row_height))
            pygame.draw.line(screen, border_color, (x_start, y + row_height), (x_start + sum(col_widths), y + row_height), 2)
            x = x_start
            # Mes (nombre)
            nombre_mes = nombres_meses.get(mes, mes)
            text = font.render(nombre_mes, True, WHITE)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[0]
            # Pelota
            text = font.render(str(datos['Pelota']), True, GREEN if datos['Pelota'] > 0 else GRAY)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[1]
            # ArcoD
            text = font.render(str(datos['ArcoDerecho']), True, GREEN if datos['ArcoDerecho'] > 0 else GRAY)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[2]
            # ArcoI
            text = font.render(str(datos['ArcoIzquierdo']), True, GREEN if datos['ArcoIzquierdo'] > 0 else GRAY)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[3]
            # Bot
            text = font.render(str(datos['Bot']), True, GREEN if datos['Bot'] > 0 else GRAY)
            screen.blit(text, (x + 10, y + 5))
            x += col_widths[4]
            y += row_height

        # Dibujar borde exterior de la tabla
        pygame.draw.rect(screen, border_color, (x_start, 100, sum(col_widths), y - 100), 3, border_radius=10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# ------------------- LOOP PRINCIPAL -------------------
while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected = (selected + 1) % len(options)
            elif event.key == pygame.K_UP:
                selected = (selected - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected == 0:
                    mostrar_resumen()
                elif selected == 1:
                    mostrar_registro_por_anio_mes()
