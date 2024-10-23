from flask import Flask, session, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion'

# Inicializar productos en la sesión
def inicializar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Ruta principal para la gestión de productos
@app.route('/')
def gestion_productos():
    inicializar_sesion()
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/nuevo_producto', methods=['POST'])
def nuevo_producto():
    inicializar_sesion()
    productos = session['productos']
    nuevo_id = len(productos) + 1
    producto = {
        'id': nuevo_id,
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'categoria': request.form['categoria'],
        'fecha_vencimiento': request.form['fecha_vencimiento']
    }
    productos.append(producto)
    session['productos'] = productos
    return redirect(url_for('gestion_productos'))

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [p for p in productos if p['id'] != id]
    return redirect(url_for('gestion_productos'))

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['categoria'] = request.form['categoria']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        session['productos'] = productos
        return redirect(url_for('gestion_productos'))
    
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
