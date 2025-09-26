import pygame
import sys
from config import BLANCO, WIDTH, HEIGHT, ventana, ROJO, FPS, clock, fuente, fondoMenuResponsive, fuente_chica

pygame.init()
def login_usuario():
    nombre = ""
    password = ""
    ingresando_password = False
    logueando = True
    error = ""
    usuario_logueado = None

    # Leer usuarios existentes con formato id,nombre,contraseña
    try:
        with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
            usuarios = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        usuarios = []

    while logueando:
        ventana.blit(fondoMenuResponsive, (0, 0))

        # Título
        titulo = fuente.render("Login de usuario", True, BLANCO)
        ventana.blit(titulo, ((WIDTH - titulo.get_width()) // 2, HEIGHT // 6))

        # Instrucción
        instruccion = fuente_chica.render(
            "Ingresa tu nombre y contraseña (ENTER para continuar)", True, BLANCO
        )
        ventana.blit(instruccion, ((WIDTH - instruccion.get_width()) // 2, HEIGHT // 3))

        # Campo de texto
        texto = nombre if not ingresando_password else "*" * len(password)
        label = "Nombre: " if not ingresando_password else "Contraseña: "
        nombre_render = fuente_chica.render(label + texto, True, ROJO)
        ventana.blit(nombre_render, ((WIDTH - nombre_render.get_width()) // 2, HEIGHT // 2))

        # Mensaje de error
        if error:
            error_render = fuente_chica.render(error, True, ROJO)
            ventana.blit(error_render, ((WIDTH - error_render.get_width()) // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not ingresando_password and nombre.strip():
                        ingresando_password = True
                    elif ingresando_password and password.strip():
                        # Validar login
                        for u in usuarios:
                            uid, n, p = u[:3]  # id, nombre y contraseña
                            if n == nombre.strip() and p == password.strip():
                                usuario_logueado = int(uid)
                                logueando = False
                                break
                        else:  # se ejecuta si no se encontró coincidencia
                            error = "Usuario o contraseña incorrectos."
                            nombre = ""
                            password = ""
                            ingresando_password = False

                elif event.key == pygame.K_BACKSPACE:
                    if not ingresando_password:
                        nombre = nombre[:-1]
                    else:
                        password = password[:-1]

                elif event.key == pygame.K_ESCAPE:
                    logueando = False
                    error = ""

                else:
                    if not ingresando_password:
                        if len(nombre) < 20 and event.unicode.isprintable():
                            nombre += event.unicode
                    else:
                        if len(password) < 20 and event.unicode.isprintable():
                            password += event.unicode

        clock.tick(FPS)

    return usuario_logueado


def registro_usuario():
    nombre = ""
    password = ""
    registrando = True
    ingresando_password = False
    error = ""

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
        ventana.blit(fondoMenuResponsive, (0, 0))
        titulo = fuente.render("Registro de usuario", True, BLANCO)
        ventana.blit(titulo, ((WIDTH - titulo.get_width()) // 2, HEIGHT // 6))

        if not ingresando_password:
            instruccion = fuente_chica.render("Escribe tu nombre y presiona ENTER", True, BLANCO)
            texto = nombre
        else:
            instruccion = fuente_chica.render("Escribe tu contraseña y presiona ENTER", True, BLANCO)
            texto = "*" * len(password)

        ventana.blit(instruccion, ((WIDTH - instruccion.get_width()) // 2, HEIGHT // 3))

        nombre_render = fuente_chica.render(texto, True, ROJO)
        ventana.blit(nombre_render, ((WIDTH - nombre_render.get_width()) // 2, HEIGHT // 2))

        if error:
            error_render = fuente_chica.render(error, True, ROJO)
            ventana.blit(error_render, ((WIDTH - error_render.get_width()) // 2, HEIGHT // 2 + 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not ingresando_password and nombre.strip():
                        if nombre.strip() in usuarios:
                            error = "¡Ese usuario ya existe! Escribe otro."
                            nombre = ""
                        else:
                            ingresando_password = True
                    elif ingresando_password and password.strip():
                        nuevo_id = ultimo_id + 1
                        with open("./utils/regist/usuarios.txt", "a", encoding="utf-8") as f:
                            f.write(f"{nuevo_id},{nombre.strip()},{password.strip()}\n")
                        registrando = False

                elif event.key == pygame.K_BACKSPACE:
                    if not ingresando_password:
                        nombre = nombre[:-1]
                    else:
                        password = password[:-1]

                elif event.key == pygame.K_ESCAPE:
                    registrando = False
                    error = ""

                else:
                    if not ingresando_password:
                        if len(nombre) < 20 and event.unicode.isprintable():
                            nombre += event.unicode
                    else:
                        if len(password) < 20 and event.unicode.isprintable():
                            password += event.unicode

        clock.tick(FPS)

    return not registrando

from datetime import datetime

def registrar_resultado(user_id, resultado, archivo="./utils/regist/resultados.txt"):
    fecha = datetime.now().strftime("%Y-%m-%d")  # Solo fecha
    try:
        with open(archivo, "a", encoding="utf-8") as f:
            f.write(f"{user_id},{resultado},{fecha}\n")
    except Exception as e:
        print("❌ Error al registrar resultado:", e)
