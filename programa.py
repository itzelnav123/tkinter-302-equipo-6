#JUAREZ NAVA MARINA ITZEL: sube el programa inicial
import tkinter as tk

from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",

        
        database="total_productos"
    )

def obtener_datos():
    nombres = [
        entry_nombre1.get().strip(),
        entry_nombre2.get().strip(),
        entry_nombre3.get().strip()
    ]

    precios = [
        entry_precio1.get().strip(),
        entry_precio2.get().strip(),
        entry_precio3.get().strip()
    ]

    if any(nombre == "" for nombre in nombres):
        messagebox.showwarning("Aviso", "Falta ingresar el nombre de un producto.")
        return None

    if any(precio == "" for precio in precios):
        messagebox.showwarning("Aviso", "Falta ingresar un precio.")
        return None

    try:
        precios = [float(precio) for precio in precios]

        if any(precio < 0 for precio in precios):
            messagebox.showwarning("Aviso", "Los precios no pueden ser negativos.")
            return None

    except ValueError:
        messagebox.showwarning("Aviso", "Los precios deben ser números.")
        return None

    total = sum(precios)
    return nombres, precios, total

def mostrar_total():
    datos = obtener_datos()

    if datos is None:
        return

    nombres, precios, total = datos

    resultado.set(
        f"{nombres[0]}: ${precios[0]:.2f}\n"
        f"{nombres[1]}: ${precios[1]:.2f}\n"
        f"{nombres[2]}: ${precios[2]:.2f}\n"
        f"TOTAL: ${total:.2f}"
    )

def guardar():
    datos = obtener_datos()

    if datos is None:
        return

    nombres, precios, total = datos

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """INSERT INTO productos
        (nombre1, precio1, nombre2, precio2,
        nombre3, precio3, total)
        VALUES (%s,%s,%s,%s,%s,%s,%s)"""

        valores = (
            nombres[0], precios[0],
            nombres[1], precios[1],
            nombres[2], precios[2], total
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        mostrar_total()
        consultar()

        messagebox.showinfo("Correcto", "Productos guardados.")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

def consultar():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM productos")
        registros = cursor.fetchall()

        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for registro in registros:
            tabla.insert("", "end", values=registro)

        cursor.close()
        conexion.close()

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

id_seleccionado = None

def seleccionar(event):
    global id_seleccionado

    seleccion = tabla.selection()

    if not seleccion:
        return

    registro = tabla.item(seleccion[0], "values")
    id_seleccionado = int(registro[0])

    entradas = [
        entry_nombre1, entry_precio1,
        entry_nombre2, entry_precio2,
        entry_nombre3, entry_precio3
    ]

    valores = [
        registro[1], registro[2],
        registro[3], registro[4],
        registro[5], registro[6]
    ]

    for entrada, valor in zip(entradas, valores):
        entrada.delete(0, tk.END)
        entrada.insert(0, valor)

    resultado.set(
        f"{registro[1]}: ${float(registro[2]):.2f}\n"
        f"{registro[3]}: ${float(registro[4]):.2f}\n"
        f"{registro[5]}: ${float(registro[6]):.2f}\n"
        f"TOTAL: ${float(registro[7]):.2f}"
    )

def actualizar():
    global id_seleccionado

    if id_seleccionado is None:
        messagebox.showwarning("Aviso", "Selecciona un registro.")
        return

    datos = obtener_datos()

    if datos is None:
        return

    nombres, precios, total = datos

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """UPDATE productos SET
        nombre1=%s, precio1=%s,
        nombre2=%s, precio2=%s,
        nombre3=%s, precio3=%s,
        total=%s WHERE id=%s"""

        valores = (
            nombres[0], precios[0],
            nombres[1], precios[1],
            nombres[2], precios[2],
            total, id_seleccionado
        )

        cursor.execute(sql, valores)
        conexion.commit()

        cursor.close()
        conexion.close()

        consultar()
        messagebox.showinfo("Correcto", "Registro actualizado.")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

def eliminar():
    global id_seleccionado

    if id_seleccionado is None:
        messagebox.showwarning("Aviso", "Selecciona un registro.")
        return

    if not messagebox.askyesno("Confirmar", "¿Deseas eliminar este registro?"):
        return

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM productos WHERE id=%s",
            (id_seleccionado,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        limpiar()
        consultar()

        messagebox.showinfo("Correcto", "Registro eliminado.")

    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))

# Gutierrez Romero Valentina: Botón Limpiar
def limpiar():
    global id_seleccionado

    entradas = [
        entry_nombre1, entry_precio1,
        entry_nombre2, entry_precio2,
        entry_nombre3, entry_precio3
    ]

    for entrada in entradas:
        entrada.delete(0, tk.END)

    resultado.set("")
    id_seleccionado = None
    tabla.selection_remove(tabla.selection())

ventana = tk.Tk()
ventana.title("Total de productos")
ventana.geometry("950x700")
ventana.configure(bg="#F1F5F9")
ventana.resizable(True, True)

titulo = tk.Label(
    ventana,
    text="TOTAL DE PRODUCTOS",
    font=("Arial", 20, "bold"),
    bg="#14243A",
    fg="white",
    pady=15
)
titulo.pack(fill="x")

marco = tk.Frame(ventana, bg="#F1F5F9")
marco.pack(pady=20)

tk.Label(marco, text="Producto", font=("Arial", 11, "bold"), bg="#F1F5F9").grid(row=0, column=0, padx=15, pady=10)
tk.Label(marco, text="Nombre", font=("Arial", 11, "bold"), bg="#F1F5F9").grid(row=0, column=1, padx=15)
tk.Label(marco, text="Precio", font=("Arial", 11, "bold"), bg="#F1F5F9").grid(row=0, column=2, padx=15)

entry_nombre1 = tk.Entry(marco, width=25, font=("Arial", 11))
entry_precio1 = tk.Entry(marco, width=15, font=("Arial", 11))

entry_nombre2 = tk.Entry(marco, width=25, font=("Arial", 11))
entry_precio2 = tk.Entry(marco, width=15, font=("Arial", 11))

entry_nombre3 = tk.Entry(marco, width=25, font=("Arial", 11))
entry_precio3 = tk.Entry(marco, width=15, font=("Arial", 11))

entradas = [
    (entry_nombre1, entry_precio1),
    (entry_nombre2, entry_precio2),
    (entry_nombre3, entry_precio3)
]

for i, (nombre, precio) in enumerate(entradas):
    tk.Label(marco, text=f"Producto {i+1}", bg="#F1F5F9").grid(row=i+1, column=0, padx=15, pady=8)
    nombre.grid(row=i+1, column=1, padx=15, pady=8)
    precio.grid(row=i+1, column=2, padx=15, pady=8)

resultado = tk.StringVar()

etiqueta_resultado = tk.Label(
    ventana,
    textvariable=resultado,
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#14243A",
    width=45,
    height=5,
    justify="left"
)
etiqueta_resultado.pack(pady=10)

marco_botones = tk.Frame(ventana, bg="#F1F5F9")
marco_botones.pack(pady=10)

tk.Button(marco_botones, text="Total", command=mostrar_total, bg="#2563EB", fg="white", width=12).grid(row=0, column=0, padx=4)
tk.Button(marco_botones, text="Guardar", command=guardar, bg="#059669", fg="white", width=12).grid(row=0, column=1, padx=4)
tk.Button(marco_botones, text="Consultar", command=consultar, bg="#475569", fg="white", width=12).grid(row=0, column=2, padx=4)
tk.Button(marco_botones, text="Actualizar", command=actualizar, bg="#D97706", fg="white", width=12).grid(row=0, column=3, padx=4)
tk.Button(marco_botones, text="Eliminar", command=eliminar, bg="#DC2626", fg="white", width=12).grid(row=0, column=4, padx=4)
tk.Button(marco_botones, text="Limpiar", command=limpiar, bg="#64748B", fg="white", width=12).grid(row=0, column=5, padx=4)

tk.Label(
    ventana,
    text="REGISTROS GUARDADOS",
    font=("Arial", 13, "bold"),
    bg="#F1F5F9",
    fg="#14243A"
).pack(pady=10)

columnas = ("ID", "Nombre 1", "Precio 1", "Nombre 2", "Precio 2", "Nombre 3", "Precio 3", "Total")

tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=8)

for columna in columnas:
    tabla.heading(columna, text=columna)
    tabla.column(columna, width=105, anchor="center")

tabla.pack(padx=15, fill="x")
tabla.bind("<<TreeviewSelect>>", seleccionar)

ventana.mainloop()