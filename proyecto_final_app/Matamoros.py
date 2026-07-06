import sqlite3

# MEJORA: helpers para resumir inventario y ventas históricas

def obtener_resumen_inventario(cursor):
    cursor.execute("SELECT COUNT(*), SUM(stock), SUM(stock * precio_compra) FROM productos")
    return cursor.fetchone()


def obtener_ventas_resumen(cursor):
    cursor.execute("SELECT IFNULL(SUM(total), 0) FROM ventas WHERE DATE(fecha) = DATE('now', 'localtime')")
    ventas_hoy = cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(total), 0) FROM ventas WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now', 'localtime')")
    ventas_mes = cursor.fetchone()[0]
    return ventas_hoy, ventas_mes


def obtener_ventas_historicas(cursor):
    cursor.execute("SELECT mes_numero, total_vendido FROM historial_ventas ORDER BY mes_numero ASC")
    filas = cursor.fetchall()
    return [(fila[0], f"Mes {fila[0]}", fila[1]) for fila in filas]
