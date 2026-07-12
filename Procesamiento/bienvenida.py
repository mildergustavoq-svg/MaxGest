import customtkinter as ctk
from PIL import Image
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Sistema de gestión Comercial")
    ventana.geometry("900x550")
    ventana.resizable(False, False)

    fondo = ctk.CTkImage(
        light_image=Image.open(ASSETS_DIR / "fondo_inicio.png"),
        dark_image=Image.open(ASSETS_DIR / "fondo_inicio.png"),
        size=(900, 550),
    )

    label_fondo = ctk.CTkLabel(ventana, image=fondo, text="")
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    panel = ctk.CTkFrame(
        ventana,
        width=580,
        height=420,
        corner_radius=24,
        fg_color="#23272E",
        border_width=2,
        border_color="#2B65EC",
    )
    panel.place(relx=0.5, rely=0.5, anchor="center")

    logo = ctk.CTkImage(
        light_image=Image.open(ASSETS_DIR / "logo C.png"),
        dark_image=Image.open(ASSETS_DIR / "logo C.png"),
        size=(200, 150),
    )

    logo_label = ctk.CTkLabel(panel, image=logo, text="")
    logo_label.pack(pady=(20, 10))

    titulo = ctk.CTkLabel(
        panel,
        text="•__Sistema de Gestión Comercial__•",
        font=("Segoe UI", 32, "bold"),
    )
    titulo.pack(pady=(15, 8))

    subtitulo = ctk.CTkLabel(
        panel,
        text="Gestión de Inventario  •  Ventas  •  Reportes",
        font=("Segoe UI", 14),
        text_color="#A5B4C3",
    )
    subtitulo.pack(pady=(0, 12))

    linea = ctk.CTkFrame(panel, height=2, fg_color="#2B65EC", width=200)
    linea.pack(pady=(0, 15))

    bienvenida = ctk.CTkLabel(
        panel,
        text="¡Bienvenido!",
        font=("Segoe UI", 28, "bold"),
        text_color="#33FF99",
    )
    bienvenida.pack(pady=(10, 8))

    descripcion = ctk.CTkLabel(
        panel,
        text="Control total de tu inventario, ventas y reportes\nen un solo lugar.",
        font=("Segoe UI", 14),
        text_color="#D5D5D5",
    )
    descripcion.pack(pady=(0, 20))

    def iniciar():
        nonlocal barra, mensaje, porcentaje

        boton_iniciar.pack_forget()

        mensaje = ctk.CTkLabel(
            panel,
            text="Inicializando sistema...",
            font=("Arial", 18),
        )
        mensaje.pack(pady=30)

        barra = ctk.CTkProgressBar(panel, width=350)
        barra.pack(pady=20)
        barra.set(0)

        porcentaje = ctk.CTkLabel(panel, text="0%", font=("Arial", 16, "bold"))
        porcentaje.pack(pady=5)

        cargar()

    progreso = 0
    barra = None
    mensaje = None
    porcentaje = None

    def cargar():
        nonlocal progreso, barra, mensaje, porcentaje

        progreso += 1
        porcentaje.configure(text=f"{progreso}%")
        barra.set(progreso / 100)

        if progreso == 20:
            mensaje.configure(text="Conectando a la base de datos...")
        elif progreso == 50:
            mensaje.configure(text="Cargando modulos...")
        elif progreso == 80:
            mensaje.configure(text="Preparando interfaz")

        if progreso < 100:
            panel.after(20, cargar)
        else:
            ventana.destroy()
            try:
                from .principal import App
            except ImportError:
                from principal import App

            app = App()
            app.mainloop()

    boton_iniciar = ctk.CTkButton(
        panel,
        text="🚀  Iniciar Sistema",
        font=("Arial", 16, "bold"),
        width=240,
        height=48,
        hover_color="#1976D2",
        fg_color="#1565C0",
        corner_radius=12,
        command=iniciar,
    )
    boton_iniciar.pack(pady=(5, 20))

    version = ctk.CTkLabel(
        panel,
        text="MaxGest  •  Versión 1.0.0  •  2026",
        font=("Segoe UI", 11),
        text_color="#A5B4C3",
    )
    version.pack(side="bottom", pady=(0, 12))

    ventana.mainloop()


if __name__ == "__main__":
    main()
