import matplotlib.pyplot as plt
import sqlite3
from tkinter import messagebox

# MEJORA: funciones de gráficas que muestran un aviso en lugar de salir abruptamente

def obtener_ventas_por_hora():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    cursor.execute("""SELECT
        substr(fecha,12,2) as hora,
        SUM(total)
    FROM ventas
    WHERE length(fecha) > 10
        AND substr(fecha,1,10) = DATE('now', 'localtime')
    GROUP BY hora
    ORDER BY hora""")
    
    datos = cursor.fetchall()
    
    conexion.close()
    
    return datos

def mostrar_grafica_ventas_hoy():
    resultado = obtener_ventas_por_hora()

    if len(resultado) == 0:
        messagebox.showinfo("Ventas hoy", "No hay ventas registradas hoy.")
        return

    horas = [fila[0] for fila in resultado]
    ventas = [fila[1] for fila in resultado]

    plt.figure(figsize=(8,4))
    plt.plot(horas, ventas, marker="o")

    plt.title("Ventas por Horas")
    plt.xlabel("Horas")
    plt.ylabel("Monto vendido")
    plt.grid(True)

    plt.show()

#mostrar_grafica_ventas_hoy()

def obtener_ventas_por_dia():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
    SELECT
        substr(fecha, 1, 10) as dia,
        SUM(total)
    FROM ventas
    WHERE substr(fecha,1,7) = substr(DATE('now', 'localtime'), 1,7)  
    GROUP BY dia
    ORDER BY dia""")
    
    diario = cursor.fetchall()
    
    conexion.close()
    return diario

def mostrar_grafica_ventas_diarias():
    resultado = obtener_ventas_por_dia()
    
    if len(resultado) == 0:
        messagebox.showinfo("Ventas diarias", "No hay ventas registradas para este mes.")
        return
        
    dias = [fila[0] for fila in resultado]
    ventas = [fila[1] for fila in resultado]
    
    plt.figure(figsize=(8,4))
    plt.plot(dias, ventas, marker="o")
    
    plt.title("Ventas Diarias del Mes")
    plt.xlabel("Días")
    plt.ylabel("Registro de ventas diarias")
    plt.grid(True)
    
    plt.show()

#mostrar_grafica_ventas_diarias()