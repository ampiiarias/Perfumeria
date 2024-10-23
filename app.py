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

@app.route('/agregar_clientes', methods=['POST'])
def agregar_clientes():
  #Obtengo los datos del formulario
  dni = request.form.get('dni')
  nombre = request.form.get('nombre')
  apellido = request.form.get('apellido')
  direccion = request.form.get('direccion')
  contacto = request.form.get('contacto')

  #los agrego a la base de datos
  query = 'INSERT INTO Cliente (dni, nombre, apellido, direccion, contacto) VALUES (%s, %s, %s, %s, %s)'
  cursor.execute(query, (dni, nombre, apellido, direccion, contacto))
  conexion.commit()
  return redirect(url_for('clientes'))

@app.route('/eliminar_clientes', methods=['POST'])
def eliminar_clientes():

  #Obtengo el id que puso en el formulario
  ID_cliente = request.form.get('ID')

  #Hago la query en la base de datos para eliminar el cliente de ese ID
  query = 'DELETE FROM Cliente WHERE '+ID_cliente+' = Cliente.ID_Cliente'
  cursor.execute(query)
  conexion.commit()
  return redirect(url_for('clientes'))

#menu productos
@app.route('/productos')
def productos():
  return render_template('productos.html')

if __name__ == '__main__':
  app.run(debug=True)