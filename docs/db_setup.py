# archivo: db_setup.py
import sqlite3

def crear_base():
    conexion = sqlite3.connect("bar.db")
    cursor = conexion.cursor()

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    # Tabla de ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER,
            fecha TEXT,
            FOREIGN KEY(producto_id) REFERENCES productos(id)
        )
    """)

    conexion.commit()
    conexion.close()
    print("✅ Base de datos creada")

crear_base()