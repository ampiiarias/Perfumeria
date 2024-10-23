from flask import *

import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
	database="proyecto_pedidos"
)
cursor = conexion.cursor()

app = Flask(__name__)

#página principal
@app.route('/')
def index():
  return render_template('index.html')


#menu pedidos
@app.route('/pedidos')
def pedidos():
  return render_template('pedidos.html')

#menu clientes
@app.route('/clientes')
def clientes():
  query = "SELECT * FROM Cliente"
  cursor.execute(query)
  clientes = cursor.fetchall()
  return render_template('clientes.html',clientes=clientes)

#menu productos
@app.route('/productos')
def productos():
  return render_template('productos.html')

if __name__ == '__main__':
  app.run(debug=True)