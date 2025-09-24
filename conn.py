from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # mismo user que usás en phpMyAdmin
        password="1234",      # misma contraseña
        database="mensajes"   # tu base creada en phpMyAdmin
    )

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT Id, mensaje FROM mensaje LIMIT 10;")
    mensajes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("index.html", mensajes=mensajes)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

