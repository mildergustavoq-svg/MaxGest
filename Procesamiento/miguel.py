import customtkinter as ctk
from tkinter import messagebox

def abrir_ventana_editar(app_principal):
    """
    Función para abrir la ventana de edición. 
    Recibe como parámetro 'app_principal' (que es el 'self' del main.py)
    para poder acceder a la base de datos y refrescar la tabla.
    """
    if not hasattr(app_principal, 'producto_eliminar_combo'):
        messagebox.showwarning("Editar", "No hay productos disponibles.")
        return

    texto = app_principal.producto_eliminar_combo.get().strip()
    if not texto:
        messagebox.showwarning("Editar", "Seleccione un producto para editar de la lista inferior.")
        return

    try:
        id_prod = int(texto.split(" - ")[0])
    except ValueError:
        messagebox.showerror("Editar", "Selección inválida.")
        return

    # para obtener datos actuales del producto usando el cursor del main
    app_principal.cursor.execute("SELECT nombre, stock, precio_compra, precio_venta FROM productos WHERE id = ?", (id_prod,))
    prod_datos = app_principal.cursor.fetchone()

    # para crear ventana emergente (Toplevel)
    ventana_edit = ctk.CTkToplevel(app_principal)
    ventana_edit.title(f"Editar Producto ID {id_prod}")
    ventana_edit.geometry("400x350")
    ventana_edit.grab_set()  #esto bloquea la ventana de atrás mientras se edita

    ctk.CTkLabel(ventana_edit, text=f"Modificando: {prod_datos[0]}", font=("Arial", 16, "bold")).pack(pady=15)

    entry_stock = ctk.CTkEntry(ventana_edit, width=200)
    entry_stock.insert(0, str(prod_datos[1]))
    entry_stock.pack(pady=10)

    entry_p_compra = ctk.CTkEntry(ventana_edit, width=200)
    entry_p_compra.insert(0, str(prod_datos[2]))
    entry_p_compra.pack(pady=10)

    entry_p_venta = ctk.CTkEntry(ventana_edit, width=200)
    entry_p_venta.insert(0, str(prod_datos[3]))
    entry_p_venta.pack(pady=10)

    def guardar_cambios():
        try:
            nuevo_stock = int(entry_stock.get())
            nuevo_pc = float(entry_p_compra.get())
            nuevo_pv = float(entry_p_venta.get())

            if nuevo_stock < 0 or nuevo_pc <= 0 or nuevo_pv <= 0:
                messagebox.showwarning("Valores Inválidos", "El stock no puede ser negativo y los precios deben ser mayores a cero.")
                return

            app_principal.cursor.execute("""
                UPDATE productos 
                SET stock = ?, precio_compra = ?, precio_venta = ? 
                WHERE id = ?
            """, (nuevo_stock, nuevo_pc, nuevo_pv, id_prod))
            app_principal.conexion.commit()

            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
            ventana_edit.destroy()
            app_principal.mostrar_productos()  #refresca la interfaz principal
        except ValueError:
            messagebox.showerror("Error", "Verifique los formatos numéricos (Enteros y Decimales).")

    ctk.CTkButton(ventana_edit, text="💾 Guardar Cambios", fg_color="#2ECC71", hover_color="#27AE60", command=guardar_cambios).pack(pady=20)


def validar_datos_alta(nombre, stock_str, pc_str, pv_str):
    """
    Valida los datos antes de insertar un nuevo producto.
    Devuelve (True, stock_int, pc_float, pv_float) si todo es correcto, o (False, None, None, None) si falla.
    """
    nombre = nombre.strip()
    if not nombre:
        messagebox.showwarning("Campo Vacío", "Ingrese una descripción de producto.")
        return False, None, None, None
    
    try:
        stock = int(stock_str)
        p_c = float(pc_str)
        p_v = float(pv_str)
        
        if stock < 0 or p_c <= 0 or p_v <= 0:
            messagebox.showwarning("Valores Inválidos", "El stock no puede ser negativo y los precios deben ser mayores a cero.")
            return False, None, None, None
            
        return True, stock, p_c, p_v
    except ValueError:
        messagebox.showerror("Error Numérico", "Verifique los formatos: Stock (Entero), Precios (Decimales).")
        return False, None, None, None