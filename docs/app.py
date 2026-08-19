import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 📌 Ruta absoluta a la base de datos dentro de la misma carpeta
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bar.db")


def get_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row  # permite acceder por nombre: fila['precio']
    return conexion


def inicializar_bd():
    """Crea la tabla e inserta productos por defecto si está vacía."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL
        )
    """)
    conexion.commit()

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
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos


# ---------------------------------------------------------
# 🏠 PANTALLA DE INICIO: elegir rol
# ---------------------------------------------------------
@app.route("/")
def inicio():
    return render_template("inicio.html")


# ---------------------------------------------------------
# 🧑‍🍳 MESERO: tomar pedidos
# ---------------------------------------------------------
pedido_actual = []
total = 0.0


@app.route("/pedidos")
def pedidos():
    productos = cargar_productos()
    return render_template("index.html", productos=productos, total=total)


@app.route("/agregar/<int:producto_id>")
def agregar(producto_id):
    global total
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio FROM productos WHERE id=?", (producto_id,))
    producto = cursor.fetchone()
    conexion.close()

    if producto:
        pedido_actual.append({"nombre": producto["nombre"], "precio": producto["precio"]})
        total += producto["precio"]

    return redirect(url_for("pedidos"))


@app.route("/pedido")
def pedido():
    return render_template("pedido.html", pedido=pedido_actual, total=total)


@app.route("/reiniciar")
def reiniciar():
    global pedido_actual, total
    pedido_actual = []
    total = 0.0
    return redirect(url_for("pedidos"))


# ---------------------------------------------------------
# 👔 GERENTE: registrar / editar / eliminar productos
# ---------------------------------------------------------
@app.route("/productos", methods=["GET", "POST"])
def productos():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", "").strip()

        error = None
        if nombre and precio:
            try:
                precio_float = float(precio)
                conexion = get_conexion()
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
                    (nombre, precio_float)
                )
                conexion.commit()
                conexion.close()
            except ValueError:
                error = "El precio debe ser un número válido."
            except sqlite3.IntegrityError:
                error = f'Ya existe un producto llamado "{nombre}".'
        else:
            error = "Nombre y precio son obligatorios."

        if error:
            lista_productos = cargar_productos()
            return render_template("productos.html", productos=lista_productos, error=error)

        return redirect(url_for("productos"))

    lista_productos = cargar_productos()
    return render_template("productos.html", productos=lista_productos)


@app.route("/productos/eliminar/<int:producto_id>")
def eliminar_producto(producto_id):
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for("productos"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
