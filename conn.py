from flask import Flask, render_template, jsonify
import mysql.connector
from informe.informeParaWeb import estadisticas_usuario
from collections import defaultdict
import json
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


ARCHIVO_RESULTADOS = './utils/regist/resultados.txt'

def analizar_resultados_usuario(user_id):
    stats_por_usuario = defaultdict(lambda: {'Ganó': 0, 'Perdió': 0, 'Empató': 0, 'Total': 0, 'Partidas_Mes': defaultdict(int)})
    
    # 1. Leer y Procesar el Archivo
    try:
        with open(ARCHIVO_RESULTADOS, 'r', encoding="utf-8") as f:
            for linea in f:
                try:
                    id_str, resultado, fecha = linea.strip().split(',')
                    current_user_id = int(id_str)
                    if current_user_id == user_id:
                        
                        mes = int(fecha.split('-')[1]) 
                        stats_por_usuario[current_user_id][resultado] += 1
                        stats_por_usuario[current_user_id]['Total'] += 1
                        stats_por_usuario[current_user_id]['Partidas_Mes'][mes] += 1
                        
                except ValueError:
                    pass 
                
    except FileNotFoundError:
        print(f"Error: El archivo '{ARCHIVO_RESULTADOS}' no fue encontrado. Asegúrate de que esté en el directorio correcto.")
        return None

    if user_id in stats_por_usuario:
        stats = stats_por_usuario[user_id]
        
        partidas_mensuales = {}
        for mes in range(1, 13):
            partidas_mensuales[mes] = stats['Partidas_Mes'].get(mes, 0)
        
        resultado_final = {
            'ID_Usuario': user_id,
            'Estadisticas': {
                'Gana': stats['Ganó'],
                'Pierde': stats['Perdió'],
                'Empate': stats['Empató'],
                'Cantidad_Partidas': stats['Total']
            },
            'Partidas_Por_Mes': partidas_mensuales
        }
        
        return resultado_final
    else:
        return None


app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # mismo user que usás en phpMyAdmin
        password="",      # misma contraseña
        database="mensaje"   # tu base creada en phpMyAdmin
    )


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mensajes')
def mensajes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT pregunta, opciones, respuesta, usuario FROM mensaje")
    mensajes = cursor.fetchall()
    for m in mensajes:
        try:
            m["opciones"] = json.loads(m["opciones"])
        except:
            m["opciones"] = []  
    
    cursor.close()
    conn.close()
    
    return render_template('mensajes.html', mensajes=mensajes)


@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/api/stats/<int:user_id>')
def estadisticas_usuario_web(user_id):
    nombre = SacarUsuario(user_id)
    datos_analizados = analizar_resultados_usuario(user_id)
    if not datos_analizados:
        return jsonify({"error": f"Usuario con ID {user_id} no encontrado (o sin partidas)."}), 404
    
    est = datos_analizados['Estadisticas']
    mensual = datos_analizados['Partidas_Por_Mes']

    resumen_mensual_lista = [mensual.get(mes, 0) for mes in range(1, 13)]

    response_json = {
        'ID_Usuario': user_id,
        'Nombre_Usuario': nombre if nombre else "Anónimo",
        'totalPartidas': est['Cantidad_Partidas'],
        'victorias': est['Gana'],
        'derrotas': est['Pierde'],
        'empates': est['Empate'],
        'resumenMeses': resumen_mensual_lista 
    }
    
    return jsonify(response_json)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
