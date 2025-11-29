import os 
from datetime import datetime


# RUTA_REGISTRO_EVENTOS = "./utils/regist/registro.txt"
# LONGITUD_ID_USUARIO = 4 # Para formatear el ID de usuario

# # --- FUNCIONES DE UTILIDAD ---

def rellenar(text, ancho, tipo="derecha_espacio"):
    text = str(text)
    if len(text) > ancho:
        return text[:ancho]
    if tipo == "izquierda":
        return text.zfill(ancho)
    elif tipo == "derecha_espacio":
        return text.ljust(ancho)
    else: # Por defecto: derecha con espacio
        return text.ljust(ancho)


class PunteroObj:
    def __init__(self): 
        self.COLUMNAS_EVENTOS = {
            "IdReg": 5,           
            "IdUser": 4,          
            "Fecha": 10,         
            "Evento": 12,       
            "X": 4,              
            "Y": 4,              
            "sig": 5,             
            "ant": 5              
        }

        self.COLUMNAS_RESULTADOS = {
            "IdReg": 5,           
            "IdUser": 4,          
            "Fecha": 10,         
            "Resultado": 12,                
            "sig": 5,             
            "ant": 5              
        }

        self.COLUMNAS_USUARIO = {
            "IdUsuario": 2,                    
            "Nombre": 18,         
            "Contraseña": 18,       
            "IResultado": 5,              
            "FResultado": 5,   
            "IEvento": 5,              
            "FEvento": 5,                     
        }
        # 1 eventos 2 resultados 3 totalEventos
        self.RUTAS = [
            "./utils/puntero/eventos.txt",
            "./utils/puntero/resultados.txt",
            "./utils/regist/usuarios.txt"
        ]
    def calcular(self, columnas, typeRuta):
        try:
            result = sum(columnas.values())
            resultColumna = (result + len(columnas) - 1)+2
            ruta = self.RUTAS[typeRuta]
            tamaño_archivo = os.path.getsize(ruta)
            tamañoTotalRegistros = tamaño_archivo // resultColumna
            return tamañoTotalRegistros, resultColumna

        except FileNotFoundError:
            print("Archivo no encontrado.")

    def registrarEvento(self, id_usuario, fecha, evento, x=0, y=0):
        cantidadRegistros,  resultColumna = self.calcular(self.COLUMNAS_EVENTOS, 0)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)
        nuevoIdReg = cantidadRegistros + 1

        # actualizar I y F en archivo usuario
        # 01,agustincito       ,123               ,00000,00000,00000,00000,00000,00000 
        # id, usuario, password, IResultado, FResultado, IEvento, FEvento, 
        # 0     1       2           3           4          5         6         

        # actualizar IEvento y FEvento en archivo usuario con seek

        with open(self.RUTAS[2], "rb") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_evento = int(registro_usuario[5])
            fin_evento = int(registro_usuario[6])

            if inicio_evento == 0:
                newinicio_evento = nuevoIdReg
                newfin_evento = nuevoIdReg
            else:
                newinicio_evento = inicio_evento
                newfin_evento = nuevoIdReg

            registro_usuario[5] = rellenar(newinicio_evento, self.COLUMNAS_USUARIO["IEvento"], "izquierda")
            registro_usuario[6] = rellenar(newfin_evento, self.COLUMNAS_USUARIO["FEvento"], "izquierda")

            registro_usuario = ",".join(registro_usuario)

        with open(self.RUTAS[2], "r+b") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            archivo_usuario.write(registro_usuario.encode("utf-8"))

        # registrar evento en archivo eventos

        if inicio_evento == 0 and fin_evento == 0:
            registro_formateado = (
                rellenar(nuevoIdReg, self.COLUMNAS_EVENTOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.COLUMNAS_EVENTOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.COLUMNAS_EVENTOS["Fecha"], "derecha_espacio") + "," +
                rellenar(evento, self.COLUMNAS_EVENTOS["Evento"], "derecha_espacio") + "," +
                rellenar(x, self.COLUMNAS_EVENTOS["X"], "izquierda") + "," +
                rellenar(y, self.COLUMNAS_EVENTOS["Y"], "izquierda") + "," + 
                rellenar("00000", self.COLUMNAS_EVENTOS["sig"], "izquierda") + "," +
                rellenar("00000", self.COLUMNAS_EVENTOS["ant"], "izquierda") + "\n"
            )
        else:
            #conseguir el id del ultimo registro para actualizar su campo 
            with open(self.RUTAS[0], "r+b") as archivo_eventos:
                archivo_eventos.seek((resultColumna * fin_evento) - resultColumna) 
                registro_anterior = archivo_eventos.read(resultColumna).decode("utf-8").strip().split(",")
                index = registro_anterior[0]
                registro_anterior[-1] = rellenar(nuevoIdReg, self.COLUMNAS_EVENTOS["sig"], "izquierda")
                registro_anterior = ",".join(registro_anterior)
                archivo_eventos.seek((resultColumna * fin_evento) - resultColumna) 
                archivo_eventos.write(registro_anterior.encode("utf-8"))

            registro_formateado = (
                rellenar(nuevoIdReg, self.COLUMNAS_EVENTOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.COLUMNAS_EVENTOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.COLUMNAS_EVENTOS["Fecha"], "derecha_espacio") + "," +
                rellenar(evento, self.COLUMNAS_EVENTOS["Evento"], "derecha_espacio") + "," +
                rellenar(x, self.COLUMNAS_EVENTOS["X"], "izquierda") + "," +
                rellenar(y, self.COLUMNAS_EVENTOS["Y"], "izquierda") + "," + 
                rellenar(index, self.COLUMNAS_EVENTOS["sig"], "izquierda") + "," +
                rellenar("00000", self.COLUMNAS_EVENTOS["ant"], "izquierda") + "\n"
            )

        with open(self.RUTAS[0], "a") as archivo_eventos:
            archivo_eventos.write(registro_formateado)

        pass

    
    def sacar_usuario(self, id):
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)

        try:
            with open(self.RUTAS[2], 'rb') as f:
                f.seek((id * resultadoColumnaU)- resultadoColumnaU) 
                registro = f.read(resultadoColumnaU).decode("utf-8").strip().split(",")
                return registro
            
        except FileNotFoundError:
            print(f"Error: El archivo '{self.RUTAS[2]}' no fue encontrado. Asegúrate de que esté en el directorio correcto.")
            return None

        pass

    def getColisiones(self, id_usuario):
        cantidadRegistros,  resultColumna = self.calcular(self.COLUMNAS_EVENTOS, 0)
        usuario = self.sacar_usuario(id_usuario)

        if usuario is None:
            return []

        inicio_resultado = int(usuario[4])
        fin_resultado = int(usuario[5])


        print(fin_resultado)

        ANIO_INICIO = 2025
        CANT_ANIOS = 5
        MESES = 12
        ## matriz[anio][mes][{cantidadResultados,victorias,derrotas,empates}]

        matriz = [
            [
                {
                    "cantidadColisiones": 0,
                    "bot": 0,
                    "arcoDerecho": 0,
                    "arcoIzquierdo": 0,
                    "pelota": 0,
                }
                for _ in range(MESES)
            ]
            for _ in range(CANT_ANIOS)
        ]

        if inicio_resultado == 0 and fin_resultado == 0:
            return 0, 0
        try:
            with open(self.RUTAS[0], 'rb') as f:
                while True:
                    f.seek(resultColumna * (inicio_resultado - 1))
                    registro = f.read(resultColumna).decode("utf-8").strip().split(",")

                    if int(registro[-1]) != 0:
                        fecha_str = registro[2].strip()
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                        anio_index = fecha.year - ANIO_INICIO
                        mes_index = fecha.month - 1
                        if registro[3].strip() == "Pelota":
                            matriz[anio_index][mes_index]["pelota"] += 1
                        elif registro[3].strip() == "ArcoIzquierd":
                            matriz[anio_index][mes_index]["arcoIzquierdo"] += 1
                        elif registro[3].strip() == "ArcoDerecho":
                            matriz[anio_index][mes_index]["arcoDerecho"] += 1
                        elif registro[3].strip() == "Bot":
                            matriz[anio_index][mes_index]["bot"] += 1

                        matriz[anio_index][mes_index]["cantidadColisiones"] += 1

                        inicio_resultado = int(registro[-1])
                    else:


                        fecha_str = registro[2].strip()
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                        anio_index = fecha.year - ANIO_INICIO
                        mes_index = fecha.month - 1

                        if registro[3].strip() == "Pelota":
                            matriz[anio_index][mes_index]["pelota"] += 1
                        elif registro[3].strip() == "ArcoIzquierd":
                            matriz[anio_index][mes_index]["arcoIzquierdo"] += 1
                        elif registro[3].strip() == "ArcoDerecho":
                            matriz[anio_index][mes_index]["arcoDerecho"] += 1
                        elif registro[3].strip() == "Bot":
                            matriz[anio_index][mes_index]["bot"] += 1

                        matriz[anio_index][mes_index]["cantidadColisiones"] += 1
                        break
                    
            return matriz

        except FileNotFoundError:
            print(f"Error: El archivo '{self.RUTAS[0]}' no fue encontrado. Asegúrate de que esté en el directorio correcto.")
            return []

        pass


    def getResultadosUsuario(self, id_usuario):
        cantidadRegistros,  resultColumna = self.calcular(self.COLUMNAS_RESULTADOS, 1)
        usuario = self.sacar_usuario(id_usuario)

        if usuario is None:
            return []

        inicio_resultado = int(usuario[4])
        fin_resultado = int(usuario[5])


        print(fin_resultado)

        ANIO_INICIO = 2025
        CANT_ANIOS = 5
        MESES = 12
        ## matriz[anio][mes][{cantidadResultados,victorias,derrotas,empates}]

        matriz = [
            [
                {
                    "cantidadResultados": 0,
                    "victorias": 0,
                    "derrotas": 0,
                    "empates": 0
                }
                for _ in range(MESES)
            ]
            for _ in range(CANT_ANIOS)
        ]

        if inicio_resultado == 0 and fin_resultado == 0:
            return 0, 0
        try:
            with open(self.RUTAS[1], 'rb') as f:
                while True:
                    f.seek(resultColumna * (inicio_resultado - 1))
                    registro = f.read(resultColumna).decode("utf-8").strip().split(",")

                    if int(registro[-1]) != 0:
                        fecha_str = registro[2].strip()
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                        anio_index = fecha.year - ANIO_INICIO
                        mes_index = fecha.month - 1
                        if registro[3].strip() == "W":
                            matriz[anio_index][mes_index]["victorias"] += 1
                        elif registro[3].strip() == "L":
                            matriz[anio_index][mes_index]["derrotas"] += 1
                        elif registro[3].strip() == "N":
                            matriz[anio_index][mes_index]["empates"] += 1
                        matriz[anio_index][mes_index]["cantidadResultados"] += 1
                        inicio_resultado = int(registro[-1])
                    else:


                        fecha_str = registro[2].strip()
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                        anio_index = fecha.year - ANIO_INICIO
                        mes_index = fecha.month - 1

                        if registro[3].strip() == "W":
                            matriz[anio_index][mes_index]["victorias"] += 1
                        elif registro[3].strip() == "L":
                            matriz[anio_index][mes_index]["derrotas"] += 1
                        elif registro[3].strip() == "N":
                            matriz[anio_index][mes_index]["empates"] += 1
                        matriz[anio_index][mes_index]["cantidadResultados"] += 1
                        break
                    
            return matriz

        except FileNotFoundError:
            print(f"Error: El archivo '{self.RUTAS[1]}' no fue encontrado. Asegúrate de que esté en el directorio correcto.")
            return []

        pass
    
    def registrarResultado(self, id_usuario, fecha, resultado):
        cantidadRegistros,  resultColumna = self.calcular(self.COLUMNAS_RESULTADOS, 1)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)
        nuevoIdReg = cantidadRegistros + 1
        # actualizar I y F en archivo usuario
        # 01,agustincito       ,123               ,00000,00000,00000,00000,00000,00000 
        # id, usuario, password, IResultado, FResultado, IEvento, FEvento 
        # 0     1       2           3           4          5         6                 

        # actualizar FResultado IResultado en archivo usuario con seek

        with open(self.RUTAS[2], "rb") as archivo_usuario:

            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_resultado = int(registro_usuario[3])
            fin_resultado = int(registro_usuario[4])

            if inicio_resultado == 0:
                newinicio_resultado = nuevoIdReg
                newfin_resultado = nuevoIdReg
            else:
                newinicio_resultado = inicio_resultado
                newfin_resultado = nuevoIdReg

            registro_usuario[3] = rellenar(newinicio_resultado, self.COLUMNAS_USUARIO["IResultado"], "izquierda")
            registro_usuario[4] = rellenar(newfin_resultado, self.COLUMNAS_USUARIO["FResultado"], "izquierda")

            registro_usuario = ",".join(registro_usuario)

        with open(self.RUTAS[2], "r+b") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            archivo_usuario.write(registro_usuario.encode("utf-8"))

        # registrar evento en archivo eventos
        # COLUMNAS_RESULTADOS = {
        #     "IdReg": 5,           
        #     "IdUser": 4,          
        #     "Fecha": 10,         
        #     "Resultado": 12,                
        #     "sig": 5,             
        #     "ant": 5              
        # }

        if inicio_resultado == 0 and fin_resultado == 0:
            registro_formateado = (
                rellenar(nuevoIdReg, self.COLUMNAS_RESULTADOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.COLUMNAS_RESULTADOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.COLUMNAS_RESULTADOS["Fecha"], "derecha_espacio") + "," +
                rellenar(resultado, self.COLUMNAS_RESULTADOS["Resultado"], "derecha_espacio") + "," +
                rellenar("00000", self.COLUMNAS_RESULTADOS["sig"], "izquierda") + "," +
                rellenar("00000", self.COLUMNAS_RESULTADOS["ant"], "izquierda") + "\n"
            )
        else:
            #conseguir el id del ultimo registro para actualizar su campo 
            with open(self.RUTAS[1], "r+b") as archivo_eventos:
                archivo_eventos.seek((resultColumna * fin_resultado) - resultColumna) 
                registro_anterior = archivo_eventos.read(resultColumna).decode("utf-8").strip().split(",")
                print(registro_anterior)
                index = registro_anterior[0]
                registro_anterior[-1] = rellenar(nuevoIdReg, self.COLUMNAS_RESULTADOS["sig"], "izquierda")
                registro_anterior = ",".join(registro_anterior)
                archivo_eventos.seek((resultColumna * fin_resultado) - resultColumna) 
                archivo_eventos.write(registro_anterior.encode("utf-8"))

            registro_formateado = (
                rellenar(nuevoIdReg, self.COLUMNAS_RESULTADOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.COLUMNAS_RESULTADOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.COLUMNAS_RESULTADOS["Fecha"], "derecha_espacio") + "," +
                rellenar(resultado, self.COLUMNAS_RESULTADOS["Resultado"], "derecha_espacio") + "," +
                rellenar(index, self.COLUMNAS_RESULTADOS["sig"], "izquierda") + "," +
                rellenar("00000", self.COLUMNAS_RESULTADOS["ant"], "izquierda") + "\n"
            )

        with open(self.RUTAS[1], "a") as archivo_eventos:
            archivo_eventos.write(registro_formateado)

        pass

