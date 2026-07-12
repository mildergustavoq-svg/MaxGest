import customtkinter as ctk
from tkinter import messagebox, filedialog
def inicializar_vista_informes(app_instance):
    """
    Renderiza la interfaz para el historial de ventas detallado
    e informes dentro del contenedor central dinámico de la App.
    """
# Limpiar la pantalla actual
    app_instance.limpiar_contenido()
# Encabezados de la sección
    ctk.CTkLabel(
        app_instance.contenido, 
        text="Historial Auditable de Ventas", 
        font=("Segoe UI", 24, "bold")
    ).pack(pady=(15, 5))
    ctk.CTkLabel(
        app_instance.contenido, 
        text="Registro detallado de transacciones comerciales con opción de exportación rápida.", 
        font=("Segoe UI", 13), 
        text_color="#A5B4C3"
    ).pack(pady=5)

# Panel de Acciones (Boton de Exportación)
    frame_acciones = ctk.CTkFrame(app_instance.contenido, fg_color="#23272E")
    frame_acciones.pack(pady=10, padx=20, fill="x")
    ctk.CTkLabel(
        frame_acciones, 
        text="Acciones de Reporte:", 
        font=("Segoe UI", 13, "bold")
    ).grid(row=0, column=0, padx=15, pady=12)
    
# Boton para exportar datos
    btn_exportar = ctk.CTkButton(
        frame_acciones, 
        text="📥 Exportar Cierre de Caja (.txt)", 
        font=("Segoe UI", 13, "bold"),
        fg_color="#3498DB", 
        hover_color="#2980B9",
        command=lambda: exportar_reporte_txt(app_instance.cursor)
    )
    btn_exportar.grid(row=0, column=1, padx=10, pady=12)

# Tabla de Datos Desplazable (Scrollable)
    tabla_ventas = ctk.CTkScrollableFrame(app_instance.contenido, height=350, fg_color="#1E222A")
    tabla_ventas.pack(fill="both", expand=True, padx=20, pady=10)
    
# Cabeceras de la tabla
    headers = [
        ("N° Transacción", 110), 
        ("Producto Vendido", 250), 
        ("Cantidad", 90), 
        ("Monto Total", 130), 
        ("Fecha y Hora", 180)
    ]
    for idx, (text, width) in enumerate(headers):
        ctk.CTkLabel(
            tabla_ventas, 
            text=text, 
            font=("Segoe UI", 13, "bold"), 
            width=width, 
            anchor="w" if idx == 1 else "center"
        ).grid(row=0, column=idx, padx=5, pady=8)

# Consulta SQL con JOIN para traer el nombre real del producto vendido
    app_instance.cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha 
        FROM ventas v
        INNER JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
    """)
    todas_ventas = app_instance.cursor.fetchall()

# Rellenar filas dinámicamente
    fila = 1
    for registro in todas_ventas:
        ctk.CTkLabel(tabla_ventas, text=f"Trans. #{registro[0]}", width=110).grid(row=fila, column=0, padx=5, pady=4)
        ctk.CTkLabel(tabla_ventas, text=str(registro[1]), width=250, anchor="w").grid(row=fila, column=1, padx=5, pady=4)
        ctk.CTkLabel(tabla_ventas, text=f"{registro[2]} und", width=90).grid(row=fila, column=2, padx=5, pady=4)
        ctk.CTkLabel(tabla_ventas, text=f"S/. {registro[3]:.2f}", width=130, text_color="#2ECC71", font=("Segoe UI", 12, "bold")).grid(row=fila, column=3, padx=5, pady=4)
        ctk.CTkLabel(tabla_ventas, text=str(registro[4]), width=180).grid(row=fila, column=4, padx=5, pady=4)
        fila += 1
    if not todas_ventas:
        ctk.CTkLabel(
            tabla_ventas, 
            text="Aún no se registran transacciones de venta en el sistema.", 
            font=("Segoe UI", 13, "italic"),
            text_color="#A5B4C3"
        ).grid(row=1, column=0, columnspan=5, pady=30)


def exportar_reporte_txt(cursor):
    """Genera un archivo plano legible con el balance consolidado de ventas."""
    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad, v.total, v.fecha 
        FROM ventas v
        INNER JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
    """)
    datos = cursor.fetchall()
    
    if not datos:
        messagebox.showwarning("Exportación Cancelada", "No hay datos de ventas disponibles para exportar.")
        return
        
    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de Texto", "*.txt")],
        title="Guardar Cierre de Caja"
    )
    
    if ruta_archivo:
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                f.write("==================================================\n")
                f.write("         REPORTE DE CIERRE DE CAJA - MAXGEST       \n")
                f.write("==================================================\n\n")
                f.write(f"Generado el: {ctk.datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 65 + "\n")
                f.write(f"{'ID':<6}{'Producto':<25}{'Cant.':<8}{'Total':<12}{'Fecha':<15}\n")
                f.write("-" * 65 + "\n")
                
                suma_acumulada = 0.0
                for r in datos:
                    f.write(f"{r[0]:<6}{r[1][:22]:<25}{r[2]:<8}S/. {r[3]:<9.2f}{r[4][:10]:<15}\n")
                    suma_acumulada += r[3]
                    
                f.write("-" * 65 + "\n")
                f.write(f"TOTAL RECAUDADO EN CAJA: S/. {suma_acumulada:.2f}\n")
                f.write("==================================================\n")
            
            messagebox.showinfo("Exportación Exitosa", f"El archivo fue guardado correctamente en:\n{ruta_archivo}")
        except Exception as e:
            messagebox.showerror("Error de Escritura", f"Ocurrió un problema al guardar el archivo: {e}")