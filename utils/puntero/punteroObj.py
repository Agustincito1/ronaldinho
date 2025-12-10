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
            "Resultado": 3,                
            "sig": 5,             
            "ant": 5              
        }

        self.JUEGOS_DIARIOS = {
            "IdReg": 5,           
            "IdUser": 4,          
            "Fecha": 10,         
            "Resultado": 2,                
            "sig": 5,             
            "ant": 5              
        }

        self.PUNTUACIONES_TOTALES = {
            "IdReg": 5,           
            "IdUser": 4,                
            "Resultado": 5,                           
        }

        self.SKINS_ADQUIRIDAS = {
            "IdReg": 5,           
            "IdUser": 4,          
            "Fecha": 10,         
            "Resultado": 5,                
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
            "IJuegosDiarios": 5,   
            "FJuegosDiarios": 5, 
            "IPuntaciones": 5, 
            "FPuntuaciones": 5, 
            "ISkins": 5, 
            "FSkins": 5,               
        }
        # 1 eventos 2 resultados 3 totalEventos
        self.RUTAS = [
            "./utils/puntero/eventos.txt",
            "./utils/puntero/resultados.txt",
            "./utils/regist/usuarios.txt",
            "./utils/regist/juegos_diarios.txt",
            "./utils/regist/puntuaciones_totales.txt"
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

    def conteoDiario(self, id_usuario, hoy):
        cantidadRegistros,  resultColumna = self.calcular(self.JUEGOS_DIARIOS, 3)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)

        with open(self.RUTAS[2], "rb") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_diario = int(registro_usuario[7])
            fin_diario = int(registro_usuario[8])
        
        with open(self.RUTAS[3], "r+b") as archivo_diarios:
            while True:
                
                archivo_diarios.seek((resultColumna * inicio_diario) - resultColumna) 
                registro = archivo_diarios.read(resultColumna).decode("utf-8").strip().split(",")
                print(registro)
                if(registro[2] == hoy):
                    conteo = int(registro[3]) + 1
                    conteo = rellenar(str(conteo), self.JUEGOS_DIARIOS["Resultado"], "izquierda")
                    registro[3] = conteo
                    registro = ",".join(registro)
                    archivo_diarios.seek((resultColumna * inicio_diario) - resultColumna) 
                    archivo_diarios.write(registro.encode("utf-8"))

                    return conteo
                else:
                    inicio_diario = int(registro[-1])

            


    def validarDiario(self, id_usuario, hoy):

        cantidadRegistros,  resultColumna = self.calcular(self.JUEGOS_DIARIOS, 3)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)

        with open(self.RUTAS[2], "rb") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_diario = int(registro_usuario[7])
            fin_diario = int(registro_usuario[8])

            while True:
                try:

                    with open(self.RUTAS[3], "rb") as archivo_diarios:
                        
                        archivo_diarios.seek((resultColumna * inicio_diario)-resultColumna)
                        registro = archivo_diarios.read(resultColumna).decode("utf-8").strip().split(",")
                        inicio_diario = int(registro[5])
                        if registro[2] == hoy:
                            if int(registro[3]) == 3:
                                return False
                            else:
                                return registro[3]
                        
                        if inicio_diario == 0:
                            break

                except OSError:
                    return True
                
            
            return "NoRegist"
            
            
    
    def getPuntajeUser(self, id_usuario):
        cantidadRegistros,  resultColumna = self.calcular(self.PUNTUACIONES_TOTALES, 4)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)
        try:

            with open(self.RUTAS[2], "rb") as archivo_usuario:
                archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
                registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
                inicio_diario = int(registro_usuario[11])
                fin_diario = int(registro_usuario[12])
                with open(self.RUTAS[4], "rb") as archivo_puntuacion:
                    archivo_puntuacion.seek((resultColumna * inicio_diario) - resultColumna) 
                    registro = archivo_puntuacion.read(resultColumna).decode("utf-8").strip().split(",")
                    puntaje = int(registro[2])
                    
                return puntaje 
        except OSError:
            return False
        


    def registrarPuntuaciones(self, id_usuario, puntaje):
        cantidadRegistros,  resultColumna = self.calcular(self.PUNTUACIONES_TOTALES, 4)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)
        nuevoIdReg = cantidadRegistros + 1

        # actualizar I y F en archivo usuario
        # 01,agustincito       ,123               ,00001,00003,00001,00113,00000,00000,00000,00000,00000,00000 
        # id, usuario, password, IResultado, FResultado, IEvento, FEvento, IJuegosDiarios, FJuegosDiarios,IPuntaciones, FPuntuaciones,ISkins, FSkins,       
        # 0     1       2           3           4          5         6       7                   8        

        # actualizar IEvento y FEvento en archivo usuario con seek

        with open(self.RUTAS[2], "rb") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_puntuacion = int(registro_usuario[9])
            fin_puntuacion= int(registro_usuario[10])
            
            if inicio_puntuacion == 0:
                newinicio_puntuacion = nuevoIdReg
                newfin_puntuacion = nuevoIdReg
            else:
                newinicio_puntuacion = inicio_puntuacion
                newfin_puntuacion = nuevoIdReg

            registro_usuario[9] = rellenar(newinicio_puntuacion, self.COLUMNAS_USUARIO["IPuntaciones"], "izquierda")
            registro_usuario[10] = rellenar(newfin_puntuacion, self.COLUMNAS_USUARIO["FPuntuaciones"], "izquierda")

            registro_usuario = ",".join(registro_usuario)

        with open(self.RUTAS[2], "r+b") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            archivo_usuario.write(registro_usuario.encode("utf-8"))

        # registrar diario en archivo juegos

        if inicio_puntuacion == 0:
            registro_formateado = (
                rellenar(nuevoIdReg, self.PUNTUACIONES_TOTALES["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.PUNTUACIONES_TOTALES["IdUser"], "izquierda") + "," +
                rellenar(puntaje, self.PUNTUACIONES_TOTALES["Resultado"], "derecha_espacio") + "\n"
            )

            with open(self.RUTAS[4], "a") as archivo_puntaje:
                archivo_puntaje.write(registro_formateado)
    
        else:
            #conseguir el id del ultimo registro para actualizar su campo 
            with open(self.RUTAS[4], "r+b") as archivo_puntaje:
                archivo_puntaje.seek((resultColumna * fin_puntuacion) - resultColumna) 
                registro_anterior = archivo_puntaje.read(resultColumna).decode("utf-8").strip().split(",")
                print(registro_anterior)
                result = int(registro_anterior[2]) + puntaje
                result = rellenar(str(result), self.PUNTUACIONES_TOTALES["Resultado"], "izquierda")
                registro_anterior[2] = result
                registro_anterior = ",".join(registro_anterior)
                archivo_puntaje.seek((resultColumna * fin_puntuacion) - resultColumna) 
                archivo_puntaje.write(registro_anterior.encode("utf-8"))



        pass

    
    def registrarJuegos(self, id_usuario, fecha, resultado):
        cantidadRegistros,  resultColumna = self.calcular(self.JUEGOS_DIARIOS, 3)
        cantidadRegistrosU, resultadoColumnaU = self.calcular(self.COLUMNAS_USUARIO, 2)
        nuevoIdReg = cantidadRegistros + 1

        # actualizar I y F en archivo usuario
        # 01,agustincito       ,123               ,00000,00000,00000,00000,00000,00000 
        # id, usuario, password, IResultado, FResultado, IEvento, FEvento, IJuegosDiarios, FJuegosDiarios,IPuntaciones, FPuntuaciones,ISkins, FSkins,       
        # 0     1       2           3           4          5         6       7                   8

        # actualizar IEvento y FEvento en archivo usuario con seek

        with open(self.RUTAS[2], "rb") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            registro_usuario = archivo_usuario.read(resultadoColumnaU).decode("utf-8").strip().split(",")
            inicio_diario = int(registro_usuario[7])
            fin_diario = int(registro_usuario[8])

            if inicio_diario == 0:
                newinicio_diario = nuevoIdReg
                newfin_diario = nuevoIdReg
            else:
                newinicio_diario = inicio_diario
                newfin_diario = nuevoIdReg

            registro_usuario[7] = rellenar(newinicio_diario, self.COLUMNAS_USUARIO["IJuegosDiarios"], "izquierda")
            registro_usuario[8] = rellenar(newfin_diario, self.COLUMNAS_USUARIO["FJuegosDiarios"], "izquierda")

            registro_usuario = ",".join(registro_usuario)

        with open(self.RUTAS[2], "r+b") as archivo_usuario:
            archivo_usuario.seek((resultadoColumnaU * id_usuario) - resultadoColumnaU) 
            archivo_usuario.write(registro_usuario.encode("utf-8"))

        # registrar diario en archivo juegos

        if inicio_diario == 0:
            registro_formateado = (
                rellenar(nuevoIdReg, self.JUEGOS_DIARIOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.JUEGOS_DIARIOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.JUEGOS_DIARIOS["Fecha"], "izquierda") + "," +
                rellenar(resultado, self.JUEGOS_DIARIOS["Resultado"], "derecha_espacio") + "," +
                rellenar("00000", self.JUEGOS_DIARIOS["sig"], "izquierda") + "," +
                rellenar("00000", self.JUEGOS_DIARIOS["ant"], "izquierda") + "\n"
            )
        else:
            #conseguir el id del ultimo registro para actualizar su campo 
            with open(self.RUTAS[3], "r+b") as archivo_eventos:
                archivo_eventos.seek((resultColumna * fin_diario) - resultColumna) 
                registro_anterior = archivo_eventos.read(resultColumna).decode("utf-8").strip().split(",")
                index = registro_anterior[0]
                registro_anterior[-1] = rellenar(nuevoIdReg, self.COLUMNAS_EVENTOS["sig"], "izquierda")
                registro_anterior = ",".join(registro_anterior)
                archivo_eventos.seek((resultColumna * fin_diario) - resultColumna) 
                archivo_eventos.write(registro_anterior.encode("utf-8"))

            registro_formateado = (
               rellenar(nuevoIdReg, self.JUEGOS_DIARIOS["IdReg"], "izquierda") + "," +
                rellenar(id_usuario, self.JUEGOS_DIARIOS["IdUser"], "izquierda") + "," +
                rellenar(fecha, self.JUEGOS_DIARIOS["Fecha"], "izquierda") + "," +
                rellenar(resultado, self.JUEGOS_DIARIOS["Resultado"], "derecha_espacio") + "," +
                rellenar(index, self.JUEGOS_DIARIOS["sig"], "izquierda") + "," +
                rellenar("00000", self.JUEGOS_DIARIOS["ant"], "izquierda") + "\n"
            )

        with open(self.RUTAS[3], "a") as archivo_juegos:
            archivo_juegos.write(registro_formateado)
    
        pass


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

        if inicio_evento == 0:
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
    # def getJuegosDiarios(self)

    def getColisiones(self, id_usuario):

        anios = set()  # usamos set para evitar repetidos

        with open(self.RUTAS[0], "r") as archivo:
            for linea in archivo:
                campos = linea.strip().split(",")  # separo por coma
                fecha = campos[2]  # la 3ra columna es la fecha
                anio = fecha.split("-")[0]  # tomo el año (YYYY)
                anios.add(int(anio))

        anios = sorted(list(anios))
        cantidadRegistros,  resultColumna = self.calcular(self.COLUMNAS_EVENTOS, 0)
        
        usuario = self.sacar_usuario(id_usuario)


        if usuario is None:
            return []

        inicio_resultado = int(usuario[5])
        fin_resultado = int(usuario[6])

        MESES = 12
        ## matriz[anio][mes][{cantidadResultados,victorias,derrotas,empates}]
        matriz = {}
        for anio in anios:

            # matriz[anio][mes][{cantidadResultados,victorias,derrotas,empates}]
            matriz[anio] = [
                {
                    "cantidadColisiones": 0,
                    "bot": 0,
                    "arcoDerecho": 0,
                    "arcoIzquierdo": 0,
                    "pelota": 0,
                }
                for _ in range(MESES)
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
                        anio_index = fecha.year 
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
                        anio_index = fecha.year 
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

        inicio_resultado = int(usuario[3])
        fin_resultado = int(usuario[4])

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

        if inicio_resultado == 0:
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

