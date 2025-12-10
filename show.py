from utils.puntero.punteroObj import PunteroObj
import os

puntero = PunteroObj()

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def rellenar(text, ancho):
    return str(text).center(ancho, " ")

    
mesesList = {
    "Enero": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Febrero": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Marzo": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Abril": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Mayo": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Junio": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Julio": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Agosto": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Septiembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Octubre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Noviembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Diciembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Total": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    }
}


mesesTotal = {
    "Enero": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Febrero": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Marzo": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Abril": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Mayo": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Junio": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Julio": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Agosto": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Septiembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Octubre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Noviembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Diciembre": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    },
    "Total": {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    }
}



inxMes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre", "Total"]
IDs = [1, 2, 3]
anios = [2025, 2026, 2027]
columnasMes = ""




for anio in anios:  
    
    
    mes_default = {
        "pelota": 0,
        "bot": 0,
        "arcoDerecho": 0,
        "arcoIzquierdo": 0
    }

    mesesList = {mes: mes_default.copy() for mes in [
        "Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre","Total"
    ]}

    mesesTotal = {mes: mes_default.copy() for mes in [
        "Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre","Total"
    ]}

    columnasMes += str(anio)+"\n"

    columnasMes += "|"+rellenar("Id User", 11) +""
    for key, value in mesesList.items():
        columnasMes += "|"+ rellenar(key, 15) 
    columnasMes += "|"

    for idUser in IDs:
        reporte = 0
        try:
            reporte = puntero.getColisiones(idUser)
            text = f"|{rellenar(idUser, 11)}"
            if anio in reporte:
                meses = reporte[anio]

                if meses:
                    for idx, colision in enumerate(meses, start=1):
                        

                        arcoDerecho = 0
                        arcoIzquierdo = 0
                        bot = 0
                        pelota = 0
                    
                        for key, value in colision.items():
                            if key == "arcoDerecho":
                                arcoDerecho += int(value)
                            elif key == "arcoIzquierdo":
                                arcoIzquierdo += int(value)   
                            elif key == "bot":
                                bot += int(value)
                            elif key == "pelota":
                                pelota += int(value)
                            

                        indexMes = inxMes[idx -1]

                        mesesList[indexMes]["arcoDerecho"] = arcoDerecho 
                        mesesList[indexMes]["arcoIzquierdo"] = arcoIzquierdo
                        mesesList[indexMes]["bot"] = bot
                        mesesList[indexMes]["pelota"] = pelota

                        mesesList["Total"]["arcoDerecho"] += arcoDerecho 
                        mesesList["Total"]["arcoIzquierdo"] += arcoIzquierdo
                        mesesList["Total"]["bot"] += bot
                        mesesList["Total"]["pelota"] += pelota

                        mesesTotal[indexMes]["arcoDerecho"]+= arcoDerecho
                        mesesTotal[indexMes]["arcoIzquierdo"] += arcoIzquierdo
                        mesesTotal[indexMes]["bot"] += bot
                        mesesTotal[indexMes]["pelota"] += pelota

                        mesesTotal["Total"]["arcoDerecho"] += arcoDerecho
                        mesesTotal["Total"]["arcoIzquierdo"] += arcoIzquierdo
                        mesesTotal["Total"]["bot"] += bot
                        mesesTotal["Total"]["pelota"] += pelota

                        
                        text += f"|{rellenar(mesesList[indexMes]['pelota'], 3)}"
                        text += f"|{rellenar(mesesList[indexMes]['bot'], 3)}"
                        text += f"|{rellenar(mesesList[indexMes]['arcoDerecho'], 3)}"
                        text += f"|{rellenar(mesesList[indexMes]['arcoIzquierdo'], 3)}"
                        
                else:
                    text += f"|{rellenar('No se encontraron colisiones para el año.', 207)}"

                text += f"|{rellenar(mesesList['Total']['pelota'], 3)}"
                text += f"|{rellenar(mesesList['Total']['bot'], 3)}"
                text += f"|{rellenar(mesesList['Total']['arcoDerecho'], 3)}"
                text += f"|{rellenar(mesesList['Total']['arcoIzquierdo'], 3)}"

                mesesList["Total"]["arcoDerecho"] = 0 
                mesesList["Total"]["arcoIzquierdo"] = 0
                mesesList["Total"]["bot"] = 0
                mesesList["Total"]["pelota"]  = 0
            else:
                text += f"|{rellenar('No hay datos disponibles para el año.', 207)}"
                continue

            columnasMes += "\n"+ text + "|"
            
        except Exception as e: 
            text += f"Ocurrió un error: {e}"



    columnasMes += "\n|"+rellenar("TOTALES", 11) +""
    for key, value in mesesTotal.items():
        for key, value in value.items():
            columnasMes += "|"+ rellenar(value, 3) 
    columnasMes += "| \n"


    with open("./show.txt", "w" ) as file:
        file.write(columnasMes)





