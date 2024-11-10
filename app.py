from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///almacen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

# Página principal (listado de productos)
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

# Página para agregar un nuevo producto
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        nuevo_producto = Producto(descripcion=descripcion, cantidad=cantidad, precio=precio)
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('form.html')

# Página para editar un producto existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.descripcion = request.form['descripcion']
        producto.cantidad = int(request.form['cantidad'])
        producto.precio = float(request.form['precio'])
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('form.html', producto=producto)

# Página para eliminar un producto
@app.route('/delete/<int:id>')
def delete(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)