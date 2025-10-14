import tkinter as tk
import sqlite3

pedido_actual = []
total = 0.0

def cargar_productos():
    conexion = sqlite3.connect("bar.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def agregar_al_pedido(nombre, precio):
    global total
    pedido_actual.append((nombre, precio))
    total += precio
    actualizar_pedido()

def actualizar_pedido():
    lista_pedido.delete(0, tk.END)
    for nombre, precio in pedido_actual:
        lista_pedido.insert(tk.END, f"{nombre} - ${precio:.2f}")
    etiqueta_total.config(text=f"🧾 Total: ${total:.2f}")

def reiniciar_pedido():
    global pedido_actual, total
    pedido_actual = []
    total = 0.0
    actualizar_pedido()
    etiqueta_total.config(text="🧾 Total: $0.00")

# Ventana principal
ventana = tk.Tk()
ventana.title("🍽️ Tomar pedido - El Rinconcito")
ventana.configure(bg="#282828")
ventana.geometry("400x600")

tk.Label(ventana, text="Selecciona productos:", font=("Arial", 14, "bold"), bg="#282828", fg="white").pack(pady=10)

frame_botones = tk.Frame(ventana, bg="#282828")
frame_botones.pack()

# Botones por producto
productos = cargar_productos()
for nombre, precio in productos:
    btn = tk.Button(frame_botones, text=f"{nombre} - ${precio:.2f}",
                    command=lambda n=nombre, p=precio: agregar_al_pedido(n, p),
                    bg="#4CAF50", fg="white", font=("Arial", 12), width=25)
    btn.pack(pady=3)

# Lista visual del pedido
tk.Label(ventana, text="🧾 Pedido actual:", font=("Arial", 12, "bold"), bg="#282828", fg="white").pack(pady=10)
lista_pedido = tk.Listbox(ventana, font=("Arial", 12), width=40)
lista_pedido.pack(pady=5)

# Total dinámico
etiqueta_total = tk.Label(ventana, text="🧾 Total: $0.00", font=("Arial", 14, "bold"), bg="#282828", fg="lightgreen")
etiqueta_total.pack(pady=10)

# Botón para reiniciar pedido
tk.Button(ventana, text="🧹 Reiniciar pedido", command=reiniciar_pedido, bg="#FF5722", fg="white", font=("Arial", 12)).pack(pady=10)

ventana.mainloop()