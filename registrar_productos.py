# archivo: registrar_productos.py
import sqlite3
import tkinter as tk

# 🛠️ Crear tabla en base de datos si no existe
def inicializar_base():
    conexion = sqlite3.connect("bar.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()
    print("✅ Base de datos lista")

# 📥 Agregar producto desde interfaz
def agregar_producto():
    nombre = entrada_nombre.get()
    precio = entrada_precio.get()

    if nombre and precio:
        try:
            conexion = sqlite3.connect("bartres.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, float(precio)))
            conexion.commit()
            conexion.close()
            resultado.config(text=f"✅ '{nombre}' agregado", fg="lightgreen")
            entrada_nombre.delete(0, tk.END)
            entrada_precio.delete(0, tk.END)
        except Exception as e:
            resultado.config(text=f"❌ Error: {e}", fg="red")
    else:
        resultado.config(text="⚠️ Ingresa nombre y precio", fg="orange")

# 📋 Mostrar productos registrados
def mostrar_productos():
    conexion = sqlite3.connect("bartres.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    ventana_lista = tk.Toplevel()
    ventana_lista.title("📋 Productos registrados")
    ventana_lista.configure(bg="#1F1F1F")

    tk.Label(ventana_lista, text="📝 Lista de productos (selecciona para copiar)",
             font=("Arial", 14, "bold"), bg="#1F1F1F", fg="white").pack(pady=10)

    cuadro_texto = tk.Text(ventana_lista, font=("Arial", 12), bg="#2E2E2E", fg="lightgray", width=40, height=15)
    cuadro_texto.pack(padx=20, pady=10)

    for nombre, precio in productos:
        cuadro_texto.insert(tk.END, f"{nombre} - ${precio:.2f}\n")

    cuadro_texto.config(state=tk.NORMAL)  # Permite copiar con Ctrl+C
# 🗑️ Eliminar producto
def eliminar_producto():
    def ejecutar_eliminacion():
        nombre_borrar = entrada_nombre_borrar.get()
        if nombre_borrar:
            conexion = sqlite3.connect("bartres.db")
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre_borrar,))
            conexion.commit()
            conexion.close()
            resultado_eliminar.config(text=f"🗑️ '{nombre_borrar}' eliminado", fg="lightgreen")
            entrada_nombre_borrar.delete(0, tk.END)
        else:
            resultado_eliminar.config(text="⚠️ Ingresa un nombre válido", fg="orange")

    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("🗑️ Eliminar producto")
    ventana_eliminar.configure(bg="#1F1F1F")

    tk.Label(ventana_eliminar, text="Nombre del producto a eliminar:", font=("Arial", 12),
             bg="#1F1F1F", fg="white").pack(pady=10)
    entrada_nombre_borrar = tk.Entry(ventana_eliminar, font=("Arial", 12))
    entrada_nombre_borrar.pack()

    tk.Button(ventana_eliminar, text="Eliminar", command=ejecutar_eliminacion,
              bg="#E53935", fg="white", font=("Arial", 12)).pack(pady=10)
    resultado_eliminar = tk.Label(ventana_eliminar, text="", font=("Arial", 10), bg="#1F1F1F")
    resultado_eliminar.pack()

# 🎨 Interfaz gráfica principal
ventana = tk.Tk()
ventana.title("📦 Registro de productos - El Rinconcito")
ventana.configure(bg="#2E2E2E")
ventana.geometry("400x300")

tk.Label(ventana, text="Nombre del producto:", font=("Arial", 12),
         bg="#2E2E2E", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entrada_nombre = tk.Entry(ventana, font=("Arial", 12))
entrada_nombre.grid(row=0, column=1, padx=10)

tk.Label(ventana, text="Precio:", font=("Arial", 12),
         bg="#2E2E2E", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entrada_precio = tk.Entry(ventana, font=("Arial", 12))
entrada_precio.grid(row=1, column=1, padx=10)

tk.Button(ventana, text="📥 Agregar producto", command=agregar_producto,
          bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=2, column=1, pady=10)

tk.Button(ventana, text="📋 Ver productos", command=mostrar_productos,
          bg="#2196F3", fg="white", font=("Arial", 12)).grid(row=3, column=1)

tk.Button(ventana, text="🗑️ Eliminar producto", command=eliminar_producto,
          bg="#E53935", fg="white", font=("Arial", 12)).grid(row=4, column=1)

resultado = tk.Label(ventana, text="", font=("Arial", 10), bg="#2E2E2E")
resultado.grid(row=5, column=0, columnspan=2, pady=10)

# 🏗️ Iniciar base de datos
inicializar_base()

ventana.mainloop()