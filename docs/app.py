import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 📌 Ruta absoluta a la base de datos dentro de la misma carpeta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bar.db")


def inicializar_bd():
    """Crea la tabla e inserta productos por defecto si está vacía."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conexion.commit()

    # Verificar si existen productos
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos_semilla = [
            ("Cerveza Nacional", 45.0),
            ("Cerveza Artesanal", 75.0),
            ("Nachos con Queso", 65.0),
            ("Alitas BBQ", 120.0),
            ("Refresco 355ml", 30.0)
        ]
        cursor.executemany("INSERT INTO productos (nombre, precio) VALUES (?, ?)", productos_semilla)
        conexion.commit()

    conexion.close()


# Ejecutar inicialización al arrancar
inicializar_bd()


# 📥 Obtener productos de la base
def cargar_productos():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row  # 👈 permite acceder por nombre: producto['precio']
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos


# ➕ Agregar producto al pedido
pedido_actual = []
total = 0.0


# 🏠 Página principal: lista de productos
@app.route("/")
def index():
    productos = cargar_productos()
    return render_template("index.html", productos=productos, total=total)


@app.route("/agregar/<int:producto_id>")
def agregar(producto_id):
    global total
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row  # 👈 mismo fix aquí
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()
    conexion.close()

    if producto:
        nombre = producto["nombre"]
        precio = producto["precio"]
        pedido_actual.append({"nombre": nombre, "precio": precio})  # 👈 dict, no tupla
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
