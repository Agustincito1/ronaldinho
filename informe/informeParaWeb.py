import os

# Función para sacar nombre de usuario
def sacar_usuario(user_id):
    usuario = ""
    path = os.path.join("utils", "regist", "usuarios.txt")
    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if int(partes[0]) == int(user_id):
                if len(partes) >= 2:
                    usuario = partes[1]
    return usuario

# Función para calcular estadísticas
def estadisticas_usuario(user_id, anio=None):
    # Inicializamos contadores
    victorias = 0
    derrotas = 0
    empates = 0
    resumen_meses = [0]*12  # Enero a Diciembre

    path = os.path.join("utils", "regist", "registro.txt")
    with open(path, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) < 3:
                continue
            id_usuario, fecha, tipo = partes[:3]
            if int(id_usuario) != int(user_id):
                continue
            if anio and not fecha.startswith(str(anio)):
                continue

            # Contar victorias/derrotas/empates según tipo
            if tipo.lower() == "pelota":
                victorias += 1
            elif tipo.lower() == "bot":
                derrotas += 1
            else:
                empates += 1

            # Resumen por mes
            mes = int(fecha.split("-")[1]) - 1  # Enero=0
            resumen_meses[mes] += 1

    total_partidas = victorias + derrotas + empates
    nombre = sacar_usuario(user_id)

    return {
        "nombre": nombre,
        "totalPartidas": total_partidas,
        "victorias": victorias,
        "derrotas": derrotas,
        "empates": empates,
        "resumenMeses": resumen_meses
    }
