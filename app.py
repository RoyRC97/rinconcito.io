from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 📥 Obtener productos de la base
def cargar_productos():
    conexion = sqlite3.connect("bartres.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

# 🏠 Página principal: lista de productos
@app.route("/")
def index():
    productos = cargar_productos()
    return render_template("index.html", productos=productos)

# ➕ Agregar producto al pedido
pedido_actual = []
total = 0.0

@app.route("/agregar/<int:producto_id>")
def agregar(producto_id):
    global total
    conexion = sqlite3.connect("bartres.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()
    conexion.close()

    if producto:
        nombre, precio = producto
        pedido_actual.append((nombre, precio))
        total += precio

    return redirect(url_for("index"))

# 🧾 Ver pedido
@app.route("/pedido")
def pedido():
    return render_template("pedido.html", pedido=pedido_actual, total=total)

# 🧹 Reiniciar pedido
@app.route("/reiniciar")
def reiniciar():
    global pedido_actual, total
    pedido_actual = []
    total = 0.0
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
