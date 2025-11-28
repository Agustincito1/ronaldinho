from flask import Flask, render_template, jsonify
import mysql.connector
from informe.informeParaWeb import estadisticas_usuario
from collections import defaultdict
import json
from utils.puntero.punteroObj import PunteroObj

puntero = PunteroObj()

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
    usuario = puntero.sacar_usuario(user_id)
    datos_analizados = puntero.getResultadosUsuario(user_id)

    print(datos_analizados)
    if not datos_analizados:
        return jsonify({"error": f"Usuario con ID {user_id} no encontrado (o sin partidas)."}), 404
    

    response_json = {
        'ID_Usuario': user_id,
        'Nombre_Usuario': usuario[1].strip(),
        # 'victorias': est['Gana'],
        # 'derrotas': est['Pierde'],
        # 'empates': est['Empate'],
        # 'resumenMeses': resumen_mensual_lista 
    }
    
    return jsonify(response_json)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
