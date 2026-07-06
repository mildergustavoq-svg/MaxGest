import sqlite3
import customtkinter as ctk
from tkinter import Image, messagebox
from datetime import datetime
from Milder import mostrar_grafica_ventas_diarias
from Milder import mostrar_grafica_ventas_hoy
from Matamoros import obtener_resumen_inventario, obtener_ventas_resumen, obtener_ventas_historicas

# MEJORA: importamos helpers para el dashboard y reportes
# Configuración estética global del sistema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # === 🗄️ CONFIGURACIÓN DE BASE DE DATOS (SQLite) ===
        self.conexion = sqlite3.connect("inventario.db")
        self.cursor = self.conexion.cursor()
        
        # Creación de la tabla de productos de forma segura
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock INTEGER NOT NULL,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL
        )
        """)
        
        # Creación de la tabla histórica para la regresión de Mathias
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial_ventas (
            mes_numero INTEGER PRIMARY KEY AUTOINCREMENT,
            total_vendido REAL NOT NULL
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        total REAL NOT NULL,
        fecha TEXT NOT NULL
        )
        """)

        
        # Insertar datos base para que el módulo de reportes no falle al inicio
        self.cursor.execute("SELECT COUNT(*) FROM historial_ventas")
        if self.cursor.fetchone()[0] == 0:
            datos_iniciales = [(1, 1200.0), (2, 1450.0), (3, 1380.0), (4, 1660.0), (5, 1850.0)]
            self.cursor.executemany("INSERT INTO historial_ventas (mes_numero, total_vendido) VALUES (?, ?)", datos_iniciales)
            
        self.conexion.commit()

        # ===  CONFIGURACIÓN DE LA VENTANA PRINCIPAL ===
        self.title("Sistema de Gestión Comercial - Trabajo Final Tecsup")
        self.geometry("1050x650")

        # Menú Lateral de Navegación
        self.menu = ctk.CTkFrame(self, width=200)
        self.menu.pack(side="left", fill="y", padx=5, pady=5)

        # Contenedor Central Dinámico
        self.contenido = ctk.CTkFrame(self)
        self.contenido.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        

        # Botones de navegación del menú
        ctk.CTkButton(self.menu, text="Dashboard", command=self.mostrar_dashboard).pack(pady=10, padx=10)
        ctk.CTkButton(self.menu, text="Almacén / Productos", command=self.mostrar_productos).pack(pady=10, padx=10)
        ctk.CTkButton(self.menu, text="Registrar Ventas", command=self.mostrar_ventas).pack(pady=10, padx=10)
        ctk.CTkButton(self.menu, text="Reportes Predictivos", command=self.mostrar_reportes).pack(pady=10, padx=10)
        ctk.CTkButton(self.menu, text="Salir", fg_color="#E74C3C", hover_color="#C0392B", command=self.destroy).pack(pady=10, padx=10)
        # MEJORA: botón salir agregado al menú principal
        
        self.fila_tabla = 1
        self.mostrar_dashboard()

    def limpiar_contenido(self):
        """Limpia el contenedor central antes de renderizar una nueva pestaña."""
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # ==========================================
    #  SECCIÓN 1: DASHBOARD
    # ==========================================
    def mostrar_dashboard(self):
        self.limpiar_contenido()
        ctk.CTkLabel(self.contenido, text="Dashboard", font=("Arial", 28, "bold")).pack(pady=20)
        ctk.CTkLabel(self.contenido, text="Resumen rápido del estado general de su inventario y las ventas del negocio.", font=("Arial", 14)).pack(pady=10)
        
        # MEJORA: métricas avanzadas para el dashboard
        cuenta_prod, total_stock, capital_invertido = obtener_resumen_inventario(self.cursor)
        ventas_hoy, ventas_mes = obtener_ventas_resumen(self.cursor)
        
        cant_prod = cuenta_prod if cuenta_prod is not None else 0
        total_stock = total_stock if total_stock is not None else 0
        capital_invertido = capital_invertido if capital_invertido is not None else 0.0
        ventas_hoy = ventas_hoy if ventas_hoy is not None else 0.0
        ventas_mes = ventas_mes if ventas_mes is not None else 0.0

        # Contenedor visual de tarjetas
        frame_cards = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_cards.pack(pady=30, padx=20, fill="x")

        # Tarjeta 1: Items
        c1 = ctk.CTkFrame(frame_cards, width=220, height=120)
        c1.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(c1, text="Ítems en Catálogo", font=("Arial", 14, "italic")).pack(pady=10)
        ctk.CTkLabel(c1, text=str(cant_prod), font=("Arial", 24, "bold"), text_color="#1F6AA5").pack()

        # Tarjeta 2: Stock
        c2 = ctk.CTkFrame(frame_cards, width=220, height=120)
        c2.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(c2, text="Stock Total Almacén", font=("Arial", 14, "italic")).pack(pady=10)
        ctk.CTkLabel(c2, text=f"{total_stock} und", font=("Arial", 24, "bold"), text_color="#E67E22").pack()

        # Tarjeta 3: Capital Valorizado
        c3 = ctk.CTkFrame(frame_cards, width=220, height=120)
        c3.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(c3, text="Inversión Valorizada", font=("Arial", 14, "italic")).pack(pady=10)
        ctk.CTkLabel(c3, text=f"S/. {capital_invertido:.2f}", font=("Arial", 24, "bold"), text_color="#2ECC71").pack()

        frame_cards2 = ctk.CTkFrame(self.contenido, fg_color="transparent")
        frame_cards2.pack(pady=30, padx=20, fill="x")
        
        # MEJORA: nuevas métricas de ventas
        d1 = ctk.CTkFrame(frame_cards2, width=220, height=120)
        d1.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(d1, text="Ventas Hoy", font=("Arial", 14, "italic")).pack(pady=10)
        ctk.CTkLabel(d1, text=f"S/. {ventas_hoy:.2f}", font=("Arial", 24, "bold"), text_color="#F39C12").pack()

        d2 = ctk.CTkFrame(frame_cards2, width=220, height=120)
        d2.pack(side="left", expand=True, padx=10)
        ctk.CTkLabel(d2, text="Ventas este Mes", font=("Arial", 14, "italic")).pack(pady=10)
        ctk.CTkLabel(d2, text=f"S/. {ventas_mes:.2f}", font=("Arial", 24, "bold"), text_color="#8E44AD").pack()
        
        
        frame_interior = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )
        frame_interior.pack(fill="x", padx=20, pady=25)
        
        frame_actividad = ctk.CTkFrame(
            frame_interior,
            width=420,
            height=220,
            border_width=2,
            border_color="#2B65EC"
        )
        
        frame_actividad.pack(
            side="left",
            expand=True,
            padx=10
        )
        
        frame_stock = ctk.CTkFrame(
            frame_interior,
            width = 420,
            height = 220,
            border_width=2,
            border_color="#2B65EC"
        )
        
        frame_stock.pack(
            side="left",
            expand=True,
            padx=(10, 0)
        )
        
        ctk.CTkLabel(
            frame_actividad,
            text="ÚLtimas ventas registradas📋",
            font=("Segoe UI", 18, "bold") 
        ).pack(pady=15)
        
        ctk.CTkLabel(
            frame_stock,
            text="⚠ Stock Bajo",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)
        
        self.conexion = sqlite3.connect("inventario.db")
        self.cursor = self.conexion.cursor()
        
        self.cursor.execute("""
        SELECT total, fecha
        FROM ventas
        ORDER BY fecha DESC
        LIMIT 4""")
        
        ventas = self.cursor.fetchall()
        
        if not ventas:
            ctk.CTkLabel(
                frame_actividad,
                text="⚠️ No hay ventas registradas aún.",
                font =("Segoe UI", 13),
                text_color="#A5B4C3"
                ).pack(pady=20)
        else:
            for venta in ventas:
                ctk.CTkLabel(
                    frame_actividad,
                    text=f"• 🛒 Venta Registrada: S/. {venta[0]:.2f}",
                    font=("Segoe UI", 13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=3)
                
        self.cursor.execute("""
            SELECT nombre, stock
            FROM productos
            WHERE stock < 5
            ORDER BY stock ASC
            Limit 4""")
        
        cantidad = self.cursor.fetchall()
        
        if not cantidad:
            ctk.CTkLabel(
                frame_stock,
                text="⚠️ No hay productos con stock bajo.",
                font =("Segoe UI", 13),
                text_color="#A5B4C3"
                ).pack(pady=20)
        else:
            for producto in cantidad:
                ctk.CTkLabel(
                    frame_stock,
                    text=f"• ⚠ Producto bajo: S/. {producto[0]} (Stock: {producto[1]})",
                    font=("Segoe UI", 13),
                    anchor="w"
                ).pack(anchor="w", padx=15, pady=3)
        
    # ==========================================
    #  SECCIÓN 2: GESTIÓN DE PRODUCTOS
    # ==========================================
    def mostrar_productos(self):
        self.limpiar_contenido()
        self.fila_tabla = 1

        ctk.CTkLabel(self.contenido, text="Módulo de Inventario de Productos", font=("Arial", 24, "bold")).pack(pady=15)
        
        frame_form = ctk.CTkFrame(self.contenido)
        frame_form.pack(pady=10, padx=30, fill="x")

        self.nombre_entry = ctk.CTkEntry(frame_form, placeholder_text="Nombre del artículo", width=250)
        self.nombre_entry.grid(row=0, column=0, padx=10, pady=10)
        
        self.stock_entry = ctk.CTkEntry(frame_form, placeholder_text="Stock Inicial", width=120)
        self.stock_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.precio_compra_entry = ctk.CTkEntry(frame_form, placeholder_text="P. Compra (S/.)", width=130)
        self.precio_compra_entry.grid(row=0, column=2, padx=10, pady=10)
        
        self.precio_venta_entry = ctk.CTkEntry(frame_form, placeholder_text="P. Venta (S/.)", width=130)
        self.precio_venta_entry.grid(row=0, column=3, padx=10, pady=10)
        
        ctk.CTkButton(frame_form, text="＋ Registrar", width=120, font=("Arial", 14, "bold"), command=self.agregar_producto).grid(row=0, column=4, padx=10, pady=10)

        # MEJORA: campo de búsqueda integrado en el módulo de productos
        self.search_entry = ctk.CTkEntry(frame_form, placeholder_text="Buscar por nombre...", width=230)
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky="w")
        ctk.CTkButton(frame_form, text="Buscar", width=100, command=self.buscar_producto).grid(row=1, column=2, padx=10, pady=(0,10))
        ctk.CTkButton(frame_form, text="Mostrar todo", width=120, command=self.mostrar_productos).grid(row=1, column=3, padx=10, pady=(0,10))
        
        # Tabla con Scrollbar para los productos
        self.tabla = ctk.CTkScrollableFrame(self.contenido, height=300)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Encabezados de la tabla
        ctk.CTkLabel(self.tabla, text="ID", font=("Arial", 13, "bold"), width=50).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Descripción Producto", font=("Arial", 13, "bold"), width=300, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Stock Disp.", font=("Arial", 13, "bold"), width=100).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Costo Compra", font=("Arial", 13, "bold"), width=130).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Precio Venta", font=("Arial", 13, "bold"), width=130).grid(row=0, column=4, padx=5, pady=5)
        
        productos = self.cursor.execute("SELECT * FROM productos").fetchall()
        for prod in productos:
            ctk.CTkLabel(self.tabla, text=str(prod[0]), width=50).grid(row=self.fila_tabla, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=prod[1], width=300, anchor="w").grid(row=self.fila_tabla, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=str(prod[2]), width=100).grid(row=self.fila_tabla, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=f"S/. {prod[3]:.2f}", width=130).grid(row=self.fila_tabla, column=3, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=f"S/. {prod[4]:.2f}", width=130).grid(row=self.fila_tabla, column=4, padx=5, pady=2)
            self.fila_tabla += 1

        if productos:
            self.producto_eliminar_combo = ctk.CTkComboBox(self.contenido, values=[f"{p[0]} - {p[1]}" for p in productos], width=520)
            self.producto_eliminar_combo.pack(pady=10)
            ctk.CTkButton(self.contenido, text="Eliminar producto seleccionado", fg_color="#E74C3C", hover_color="#C0392B", command=self.eliminar_producto).pack(pady=5)
        # MEJORA: opción para eliminar productos del inventario
        
    def agregar_producto(self):
        try:
            nombre = self.nombre_entry.get().strip()
            if not nombre:
                messagebox.showwarning("Campo Vacío", "Ingrese una descripción de producto.")
                return
            
            stock = int(self.stock_entry.get())
            p_c = float(self.precio_compra_entry.get())
            p_v = float(self.precio_venta_entry.get())
            
            self.cursor.execute("INSERT INTO productos (nombre, stock, precio_compra, precio_venta) VALUES (?, ?, ?, ?)", (nombre, stock, p_c, p_v))
            self.conexion.commit()
            
            messagebox.showinfo("Éxito", "Producto guardado con éxito.")
            self.mostrar_productos()
        except ValueError:
            messagebox.showerror("Error Numérico", "Verifique los formatos: Stock (Entero), Precios (Decimales).")

    # MEJORA: búsqueda y borrado de productos
    def buscar_producto(self):
        termino = self.search_entry.get().strip()
        self.limpiar_contenido()
        self.fila_tabla = 1

        ctk.CTkLabel(self.contenido, text="Resultados de Búsqueda", font=("Arial", 24, "bold")).pack(pady=15)
        frame_form = ctk.CTkFrame(self.contenido)
        frame_form.pack(pady=10, padx=30, fill="x")

        self.nombre_entry = ctk.CTkEntry(frame_form, placeholder_text="Nombre del artículo", width=250)
        self.nombre_entry.grid(row=0, column=0, padx=10, pady=10)
        self.stock_entry = ctk.CTkEntry(frame_form, placeholder_text="Stock Inicial", width=120)
        self.stock_entry.grid(row=0, column=1, padx=10, pady=10)
        self.precio_compra_entry = ctk.CTkEntry(frame_form, placeholder_text="P. Compra (S/.)", width=130)
        self.precio_compra_entry.grid(row=0, column=2, padx=10, pady=10)
        self.precio_venta_entry = ctk.CTkEntry(frame_form, placeholder_text="P. Venta (S/.)", width=130)
        self.precio_venta_entry.grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkButton(frame_form, text="＋ Registrar", width=120, font=("Arial", 14, "bold"), command=self.agregar_producto).grid(row=0, column=4, padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(frame_form, placeholder_text="Buscar por nombre...", width=230)
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky="w")
        ctk.CTkButton(frame_form, text="Buscar", width=100, command=self.buscar_producto).grid(row=1, column=2, padx=10, pady=(0,10))
        ctk.CTkButton(frame_form, text="Mostrar todo", width=120, command=self.mostrar_productos).grid(row=1, column=3, padx=10, pady=(0,10))

        self.tabla = ctk.CTkScrollableFrame(self.contenido, height=300)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=15)

        ctk.CTkLabel(self.tabla, text="ID", font=("Arial", 13, "bold"), width=50).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Descripción Producto", font=("Arial", 13, "bold"), width=300, anchor="w").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Stock Disp.", font=("Arial", 13, "bold"), width=100).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Costo Compra", font=("Arial", 13, "bold"), width=130).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkLabel(self.tabla, text="Precio Venta", font=("Arial", 13, "bold"), width=130).grid(row=0, column=4, padx=5, pady=5)

        productos = self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{termino}%",)).fetchall()
        if not productos:
            messagebox.showinfo("Búsqueda", "No se encontraron productos con ese nombre.")
            return

        for prod in productos:
            ctk.CTkLabel(self.tabla, text=str(prod[0]), width=50).grid(row=self.fila_tabla, column=0, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=prod[1], width=300, anchor="w").grid(row=self.fila_tabla, column=1, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=str(prod[2]), width=100).grid(row=self.fila_tabla, column=2, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=f"S/. {prod[3]:.2f}", width=130).grid(row=self.fila_tabla, column=3, padx=5, pady=2)
            ctk.CTkLabel(self.tabla, text=f"S/. {prod[4]:.2f}", width=130).grid(row=self.fila_tabla, column=4, padx=5, pady=2)
            self.fila_tabla += 1

        self.producto_eliminar_combo = ctk.CTkComboBox(self.contenido, values=[f"{p[0]} - {p[1]}" for p in productos], width=520)
        self.producto_eliminar_combo.pack(pady=10)
        ctk.CTkButton(self.contenido, text="Eliminar producto seleccionado", fg_color="#E74C3C", hover_color="#C0392B", command=self.eliminar_producto).pack(pady=5)

    def eliminar_producto(self):
        if not hasattr(self, 'producto_eliminar_combo'):
            messagebox.showwarning("Eliminar", "No hay producto seleccionado.")
            return

        texto = self.producto_eliminar_combo.get().strip()
        if not texto:
            messagebox.showwarning("Eliminar", "Seleccione un producto antes de eliminar.")
            return

        try:
            id_prod = int(texto.split(" - ")[0])
        except ValueError:
            messagebox.showerror("Eliminar", "Valor inválido en el producto seleccionado.")
            return

        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el producto ID {id_prod}?")
        if confirmar:
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
            self.conexion.commit()
            messagebox.showinfo("Eliminar", "Producto eliminado correctamente.")
            self.mostrar_productos()

    # SECCIÓN 3: LOGÍSTICA DE VENTAS (Completado)
    
    def mostrar_ventas(self):
        self.limpiar_contenido()
        ctk.CTkLabel(self.contenido, text="Punto de Venta / Salida de Almacén", font=("Arial", 24, "bold")).pack(pady=20)
        
        ctk.CTkLabel(
            self.contenido,
            text="Selecciones un producto y selecciones una venta. El inventario se actualizará automáticamente.",
            font=("Segoe UI", 14),
            text_color="#A5B4C3"
        ).pack(pady=(0, 20))
        
        # Traemos solo productos que tengan unidades disponibles
        self.cursor.execute("SELECT id, nombre FROM productos WHERE stock > 0")
        lista_db = self.cursor.fetchall()
        
        # Mapeamos un diccionario de texto legible al ID de la base de datos
        self.mapeo_productos = {f"ID {p[0]} - {p[1]}": p[0] for p in lista_db}
        
        if not self.mapeo_productos:
            ctk.CTkLabel(self.contenido, text="⚠️ No hay artículos con unidades disponibles en stock.", text_color="orange", font=("Arial", 14)).pack(pady=30)
            return
        
        frame_principal = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )
        frame_principal.pack(fill="x", padx=20, pady=20)
        
        frame_ventas = ctk.CTkFrame(
            frame_principal,
            width=430,
            height=320
        )
        
        frame_ventas.pack(
            side="left",
            expand=True,
            padx=(0,10)
        )
        
        linea = ctk.CTkFrame(
            frame_principal,
            width=4,
            height= 300,
            fg_color="#2B65EC",
            corner_radius=2
        )
        linea.pack(side="left", padx=15, pady=20)
        
        frame_resumen = ctk.CTkFrame(
            frame_principal,
            width=430,
            height=320
        )
        
        frame_resumen.pack(
            side="left",
            expand=True,
            padx=(10, 0)
        )


        ctk.CTkLabel(frame_ventas, text="Seleccione el Producto a Vender:", font=("Arial", 14)).pack(pady=8)
        self.combo_productos = ctk.CTkComboBox(
            frame_ventas,
            values=list(self.mapeo_productos.keys()),
            width=400,
            command=self.actualizar_resumen)
        self.combo_productos.pack(pady=5)

        ctk.CTkLabel(frame_ventas, text="Cantidad de Unidades:", font=("Arial", 14)).pack(pady=8)
        self.cant_venta_entry = ctk.CTkEntry(frame_ventas, placeholder_text="Ejemplo: 5", width=150)
        self.cant_venta_entry.pack(pady=5)
        

        ctk.CTkButton(
            frame_ventas,
            text="🛒 Confirmar y Descontar Venta",
            font=("Arial", 14, "bold"),
            fg_color="#2ECC71",
            hover_color="#27AE60",
            command=self.procesar_venta
            ).pack(pady=25)
        
        ctk.CTkLabel(
            frame_resumen,
            text="📦Resumen de Venta",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)
        
        self.lbl_producto = ctk.CTkLabel(
            frame_resumen,
            text="Producto: -",
            font=("Segoe UI", 14)
        )
        self.lbl_producto.pack(anchor="w", padx=20, pady=8)
        
        self.lbl_precio = ctk.CTkLabel(
            frame_resumen,
            text="Precio Unitario: -",
            font=("Segoe UI", 14)
        )
        self.lbl_precio.pack(anchor="w", padx=20, pady=8)
        
        self.lbl_stock = ctk.CTkLabel(
            frame_resumen,
            text="Stock Disponible: -",
            font=("Segoe UI", 14)
        )
        self.lbl_stock.pack(anchor="w", padx=20, pady=8)
        
        self.lbl_total = ctk.CTkLabel(
            frame_resumen,
            text="Total: -",
            font=("Segoe UI", 14)
        )
        self.lbl_total.pack(anchor="w", padx=20, pady=8)
        
        self.actualizar_resumen(
            self.combo_productos.get()
        )
    
    def actualizar_resumen(self, seleccion):
            id_prod = self.mapeo_productos[seleccion]
            self.cursor.execute("""
                SELECT nombre, precio_venta, stock
                FROM productos
                WHERE id = ?
            """, (id_prod,))
            
            nombre, precio, stock = self.cursor.fetchone()
            
            self.lbl_producto.configure(
                text=f"Producto: {nombre}"
            )
            
            self.lbl_precio.configure(
                text=f"Precio Unitario: s/. {precio:.2f}"
            )
            
            self.lbl_stock.configure(
                text=f"Stock Disponible: {stock}"
            )
            
            self.lbl_total.configure(
                text=f"Total: s/ --,--"
            )

    def procesar_venta(self):
        try:
            seleccion = self.combo_productos.get()
            id_prod = self.mapeo_productos[seleccion]
            unidades = int(self.cant_venta_entry.get())
            
            if unidades <= 0:
                messagebox.showwarning("Cantidad Inválida", "La cantidad ingresada debe ser mayor a cero.")
                return

            self.cursor.execute("SELECT stock, precio_venta FROM productos WHERE id = ?", (id_prod,))
            stock_actual, precio = self.cursor.fetchone()

            if stock_actual < unidades:
                messagebox.showerror("Quiebre de Stock", f"Operación cancelada. Solo quedan {stock_actual} unidades disponibles.")
                return

            # Ecuación de balance y actualización del stock en inventario
            nuevo_stock = stock_actual - unidades
            self.cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_prod))
            
            # Sumar las ganancias al mes en curso dentro de la tabla histórica de Mathias
            monto_transaccion = unidades * precio
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.cursor.execute("""
            INSERT INTO ventas
            (producto_id, cantidad, total, fecha)
            VALUES (?, ?, ?, ?)
            """,
            (id_prod, unidades, monto_transaccion, fecha_actual))
            
            self.cursor.execute("SELECT MAX(mes_numero) FROM historial_ventas")
            ultimo_mes = self.cursor.fetchone()[0]
            
            self.cursor.execute("UPDATE historial_ventas SET total_vendido = total_vendido + ? WHERE mes_numero = ?", (monto_transaccion, ultimo_mes))
            self.conexion.commit()
            # MEJORA: actualiza la tabla histórica de ventas cada vez que se realiza una transacción

            messagebox.showinfo("Venta Exitosa", f"Venta procesada.\nTotal cobrado: S/. {monto_transaccion:.2f}")
            self.mostrar_ventas()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico entero en la cantidad.")

 
    #  SECCIÓN 4: MODELO DE REGRESIÓN DE MATHIAS (Completado)
    # MEJORA: utiliza datos históricos para calcular tendencia de ventas
  
    def mostrar_reportes(self):
        self.limpiar_contenido()
        ctk.CTkLabel(self.contenido, text="Análisis Predictivo de Ventas", font=("Arial", 26, "bold")).pack(pady=20)
        
        frame_botones = ctk.CTkFrame(self.contenido)
        frame_botones.pack(pady=10)
        
        ctk.CTkButton(
            frame_botones,
            text="Ventas por Hora",
            command=mostrar_grafica_ventas_hoy
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            frame_botones,
            text="Ventas por día",
            command=mostrar_grafica_ventas_diarias
        ).pack(side="left", padx=10)

        # Extracción de la serie de tiempo desde la base de datos
        self.cursor.execute("SELECT mes_numero, total_vendido FROM historial_ventas ORDER BY mes_numero ASC")
        datos = self.cursor.fetchall()
        n = len(datos)

        if n < 2:
            ctk.CTkLabel(self.contenido, text="Datos históricos insuficientes para calcular el modelo matemático.").pack(pady=40)
            return

        # Algoritmo de Mínimos Cuadrados para Regresión Lineal Simple
        sum_x = sum(d[0] for d in datos)
        sum_y = sum(d[1] for d in datos)
        sum_x_cuadrado = sum(d[0]**2 for d in datos)
        sum_xy = sum(d[0] * d[1] for d in datos)

        denominador = (n * sum_x_cuadrado) - (sum_x ** 2)

        if denominador == 0:
            ctk.CTkLabel(self.contenido, text="Error estadístico: División por cero en la pendiente.").pack(pady=40)
            return

        b1 = ((n * sum_xy) - (sum_x * sum_y)) / denominador
        b0 = (sum_y - (b1 * sum_x)) / n
        
        # Pronóstico del siguiente periodo en la escala del tiempo
        proximo_mes = datos[-1][0] + 1
        prediccion_final = max(0.0, b0 + (b1 * proximo_mes))

        frame_reporte = ctk.CTkFrame(self.contenido)
        frame_reporte.pack(pady=10, padx=40, fill="both", expand=True)

        ctk.CTkLabel(frame_reporte, text=f"Predicción Estimada de Facturación para el Mes N° {proximo_mes}", font=("Arial", 16, "italic")).pack(pady=20)
        ctk.CTkLabel(frame_reporte, text=f"S/. {prediccion_final:.2f}", font=("Arial", 42, "bold"), text_color="#2ECC71").pack(pady=10)
        
        # Bloque de metadatos matemáticos exigidos en los criterios de evaluación de Tecsup
        frame_meta = ctk.CTkFrame(frame_reporte, fg_color="transparent")
        frame_meta.pack(pady=30)

        ctk.CTkLabel(frame_meta, text=f"Tendencia: {'Ascendente 📈' if b1 > 0 else 'Descendente 📉'}", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=25)
        ctk.CTkLabel(frame_meta, text=f"Pendiente (b1): {b1:.4f}", font=("Arial", 14)).grid(row=0, column=1, padx=25)
        ctk.CTkLabel(frame_meta, text=f"Intercepto (b0): {b0:.2f}", font=("Arial", 14)).grid(row=0, column=2, padx=25)
        
        linea = ctk.CTkFrame(
            frame_reporte,
            width=700,
            height= 4,
            fg_color="#2B65EC",
            corner_radius=2
        )
        linea.pack(pady=20)
        
        frame_info = ctk.CTkFrame(
            frame_reporte,
            corner_radius=12,
            border_width=1,
            border_color="#2B65EC",
            fg_color="#2A2A2A"
        )
        frame_info.pack(fill="x", padx=40, pady=(20, 30))
        
        ctk.CTkLabel(
            frame_info,
            text="ℹ Información del Análisis",
            font=("Segoe UI", 18, "bold" )
        ).pack(anchor="w", padx=20, pady=(15,10))
        
        ctk.CTkLabel(
            frame_info,
            text="📈 Boton Ventas por Hora",
            font=("Segoe UI", 14, "bold"),
            text_color= "#4DA3FF"
        ).pack(anchor="w", padx=20)
        
        ctk.CTkLabel(
            frame_info,
            text="Permite visualizar el comportamiento de las ventas registradas durante cada hora del día.",
            font=("Segoe UI", 13),
            justify="left",
            text_color= "#4DA3FF",
            wraplength= 850
        ).pack(anchor="w", padx=35, pady=(0, 10))
        
        ctk.CTkLabel(
            frame_info,
            text="📊 Boton Ventas por Día",
            font=("Segoe UI", 14, "bold"),
            text_color= "#4DA3FF"
        ).pack(anchor="w", padx=20)
        
        ctk.CTkLabel(
            frame_info,
            text="Presenta la evolución diaria de las ventas y facilita el análisis histórico mediante gráficos.",
            font=("Segoe UI", 13),
            justify="left",
            text_color= "#4DA3FF",
            wraplength= 850
        ).pack(anchor="w", padx=35, pady=(0, 10))
        

if __name__ == "__main__":
    app = App()
    app.mainloop()