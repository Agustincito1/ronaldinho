from flask import Flask, render_template, jsonify
import mysql.connector
from informe.informeParaWeb import estadisticas_usuario

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
    
    cursor.execute("SELECT Id, mensaje FROM mensaje LIMIT 10;")
    mensajes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('mensajes.html', mensajes=mensajes)


@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
