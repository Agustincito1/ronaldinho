import random

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


def leerRegistros(id):
    registros = []
    with open("./utils/regist/registro.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if int(partes[0]) == int(id):
                user_id, fecha, objeto, x, y = partes
                if user_id.isdigit():
                    registros.append({
                        "user_id": user_id,
                        "fecha": fecha,
                        "objeto": objeto,
                        "x": int(x),
                        "y": int(y)
                    })

    return registros




