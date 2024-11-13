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
    query = """
        SELECT Pedido.ID_Pedido, Pedido.Fecha, Pedido.Monto, 
               Cliente.Nombre AS ClienteNombre, 
               Producto.Marca AS ProductoMarca, Producto.Nombre AS ProductoNombre
        FROM Pedido
        JOIN Cliente ON Pedido.ID_Cliente = Cliente.ID_Cliente
        JOIN Tiene ON Pedido.ID_Pedido = Tiene.ID_Pedido
        JOIN Producto ON Tiene.ID_Producto = Producto.ID_Producto;
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/eliminar_pedido', methods=['POST'])
def eliminar_pedido():
    # Obtengo el ID del pedido desde el formulario
    ID_pedido = request.form.get('ID')

    # Primero elimino las entradas en la tabla Tiene que estén relacionadas con este pedido
    query_tiene = 'DELETE FROM Tiene WHERE ID_Pedido = %s'
    cursor.execute(query_tiene, (ID_pedido,))

    # Luego elimino el pedido
    query_pedido = 'DELETE FROM Pedido WHERE ID_Pedido = %s'
    cursor.execute(query_pedido, (ID_pedido,))
    conexion.commit()

    return redirect(url_for('pedidos'))



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

@app.route('/modificar_clientes', methods=['POST'])
def modificar_clientes():
  #Obtengo el id que puso en el formulario
  ID_cliente = request.form.get('ID')

  #Obtengo los campos modificados
  dni = request.form.get('dni')
  nombre = request.form.get('nombre')
  apellido = request.form.get('apellido')
  direccion = request.form.get('direccion')
  contacto = request.form.get('contacto')

  #Ejecuto el SQL para modificar
  query = 'UPDATE Cliente SET dni = %s, nombre = %s, apellido = %s, direccion = %s, contacto = %s WHERE ID_Cliente = %s'
  cursor.execute(query, (dni,nombre,apellido,direccion,contacto,ID_cliente))
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
  query = "SELECT * FROM Producto"
  cursor.execute(query)
  productos = cursor.fetchall()
  return render_template('productos.html',productos=productos)

@app.route('/agregar_productos', methods=['POST'])
def agregar_productos():
  #Obtengo los datos del formulario
  marca = request.form.get('marca')
  nombre = request.form.get('nombre')
  medida = request.form.get('medida')
  precio = request.form.get('precio')

  #los agrego a la base de datos
  query = 'INSERT INTO Producto (marca, nombre, medida, precio) VALUES (%s, %s, %s, %s)'
  cursor.execute(query, (marca, nombre, medida, precio))
  conexion.commit()
  return redirect(url_for('productos'))

@app.route('/modificar_productos', methods=['POST'])
def modificar_productos():
  #Obtengo el id que puso en el formulario
  ID_producto = request.form.get('ID')

  #Obtengo los campos modificados
  marca = request.form.get('marca')
  nombre = request.form.get('nombre')
  medida = request.form.get('medida')
  precio = request.form.get('precio')

  #Ejecuto el SQL para modificar
  query = 'UPDATE Producto SET marca = %s, nombre = %s, medida = %s, precio = %s  WHERE ID_Producto = %s'
  cursor.execute(query, (marca,nombre,medida,precio,ID_producto))
  return redirect(url_for('productos'))

@app.route('/eliminar_productos', methods=['POST'])
def eliminar_productos():

  #Obtengo el id que puso en el formulario
  ID_producto = request.form.get('ID')

  #Hago la query en la base de datos para eliminar el producto de ese ID
  query = 'DELETE FROM Producto WHERE '+ID_producto+' = Producto.ID_Producto'
  cursor.execute(query)
  conexion.commit()
  return redirect(url_for('productos'))

if __name__ == '__main__':
  app.run(debug=True)