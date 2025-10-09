
from collections import defaultdict

def resumenCol():
    # 1. Leer usuarios y armar diccionario {id: nombre}
    usuarios = {}
    with open("./utils/regist/usuarios.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) >= 3:
                id_usuario = partes[0]
                nombre = partes[1]
                usuarios[id_usuario] = nombre

    # 2. Diccionario con la estructura de conteo
    resumen = defaultdict(lambda: {
        "Pelota": 0,
        "ArcoDerecho": 0,
        "ArcoIzquierdo": 0,
        "Bot": 0
    })

    # 3. Leer registros y acumular
    with open("./utils/regist/registro.txt", "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split(",")
            if len(partes) < 3:
                continue
            id_usuario, _, tipo, *_ = partes

            if tipo in resumen[id_usuario]:
                resumen[id_usuario][tipo] += 1

    # 4. Guardar resumen cruzado con nombre
    with open("./utils/regist/resumen.txt", "w", encoding="utf-8") as f:
        for id_usuario, datos in resumen.items():
            nombre = usuarios.get(id_usuario, "Desconocido")
            f.write(f"{id_usuario},{nombre},{datos['Pelota']},{datos['ArcoDerecho']},{datos['ArcoIzquierdo']},{datos['Bot']}\n")

    print("✅ Resumen generado en ./utils/regist/resumen.txt")