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

    # Leer usuarios existentes con formato id,nombre,contraseña,gano,perdio,empato
    try:
        with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
            usuarios = [line.strip().split(",") for line in f if line.strip()]
    except FileNotFoundError:
        usuarios = []

    while logueando:
        ventana.blit(fondoMenuResponsive, (0, 0))
        titulo = fuente.render("Login de usuario", True, BLANCO)
        ventana.blit(titulo, ((WIDTH - titulo.get_width()) // 2, HEIGHT // 6))

        instruccion = fuente_chica.render(
            "Ingresa tu nombre y contraseña (ENTER para continuar)", True, BLANCO
        )
        ventana.blit(instruccion, ((WIDTH - instruccion.get_width()) // 2, HEIGHT // 3))

        # Mostrar campo de texto
        texto = nombre if not ingresando_password else "*" * len(password)
        label = "Nombre: " if not ingresando_password else "Contraseña: "
        nombre_render = fuente_chica.render(label + texto, True, ROJO)
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
                        ingresando_password = True
                    elif ingresando_password and password.strip():
                        # Validar login
                        for u in usuarios:
                            uid, n, p, _, _, _ = u
                            if n == nombre.strip() and p == password.strip():
                                usuario_logueado = int(uid)  # ⬅ retorna el ID
                                logueando = False
                                break
                        else:
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
                            f.write(f"{nuevo_id},{nombre.strip()},{password.strip()},0,0,0\n")
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

def registrar_resultado(user_id, resultado, archivo="./utils/regist/usuarios.txt"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            lineas = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        lineas = []

    usuarios = []
    encontrado = False

    for linea in lineas:
        partes = linea.split(",")
        uid = int(partes[0])
        nombre = partes[1]
        password = partes[2]
        gano = int(partes[3])
        perdio = int(partes[4])
        empato = int(partes[5])

        if uid == user_id:  # ✅ Compara por ID
            if resultado == "Ganó":
                gano += 1
            elif resultado == "Perdió":
                perdio += 1
            elif resultado == "Empató":
                empato += 1
            encontrado = True

        usuarios.append(f"{uid},{nombre},{password},{gano},{perdio},{empato}")

    # Si no se encontró el ID, lo crea como nuevo (raro, pero por seguridad)
    if not encontrado:
        nuevo_id = int(usuarios[-1].split(",")[0]) + 1 if usuarios else 1
        gano = perdio = empato = 0
        if resultado == "Ganó":
            gano = 1
        elif resultado == "Perdió":
            perdio = 1
        elif resultado == "Empató":
            empato = 1
        usuarios.append(f"{nuevo_id},Usuario{nuevo_id},default,{gano},{perdio},{empato}")

    # Guardar de nuevo todo el archivo
    with open(archivo, "w", encoding="utf-8") as f:
        for linea in usuarios:
            f.write(linea + "\n")
